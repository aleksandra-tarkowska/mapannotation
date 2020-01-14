#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Aleksandra Tarkowska <A(dot)Tarkowska(at)dundee(dot)ac(dot)uk>,
#
# Version: 1.0

import sys
import os

from django.conf import settings
from omeroweb.settings import process_custom_settings, report_settings
from omero_mapr.utils import (
    config_list_to_dict,
    kvsubst_list_to_dict,
)


# load settings
MAPR_SETTINGS_MAPPING = {
    "omero.web.mapr.config":
        ["MAPR_CONFIG", "[]", config_list_to_dict, None],
    "omero.web.mapr.metadata_kv_substitutions":
        ["MAPR_KV_SUBST", "[]", kvsubst_list_to_dict, None],
    "omero.web.mapr.favicon":
        ["MAPR_DEFAULT_FAVICON",
         os.path.join(os.path.dirname(__file__),
                      'static', 'mapr', 'image',
                      'favicon.png').replace('\\', '/'),
         str, None],
    "omero.web.mapr.favicon_webservice":
        ["MAPR_FAVICON_WEBSERVICE",
            "http://www.google.com/s2/favicons?domain=", str, None],
    }


process_custom_settings(sys.modules[__name__], 'MAPR_SETTINGS_MAPPING')
report_settings(sys.modules[__name__])


def prefix_setting(suffix, default):
    @property
    def func(self):
        return getattr(settings, 'MAPR_%s' % suffix, default)
    return func


class MaprSettings(object):

    CONFIG = prefix_setting('CONFIG', MAPR_CONFIG)  # noqa
    KV_SUBSTS = prefix_setting('KV_SUBST',
                               MAPR_KV_SUBST)  # noqa
    DEFAULT_FAVICON = prefix_setting('DEFAULT_FAVICON',
                                     MAPR_DEFAULT_FAVICON)  # noqa
    FAVICON_WEBSERVICE = prefix_setting('FAVICON_WEBSERVICE',
                                        MAPR_FAVICON_WEBSERVICE)  # noqa


mapr_settings = MaprSettings()


# Update Django settings

# add custom processor
TEMPLATES = getattr(settings, 'TEMPLATES', [])
TEMPLATES[0]['OPTIONS']['context_processors'].append(
    'omero_mapr.custom_context_processor.mapr_url_suffix')
setattr(settings, 'TEMPLATES', TEMPLATES)
