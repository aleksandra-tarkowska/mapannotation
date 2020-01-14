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

import json
from collections import OrderedDict


def config_list_to_dict(config_list):
    config_dict = OrderedDict()
    for i in json.loads(config_list):
        k = i.get('menu', None)
        if k is not None:
            if i.get('config', None) is not None:
                config_dict[k] = i['config']
    return config_dict


def kvsubst_list_to_dict(kvsubst_list):
    kvsubst_dict = {}
    for i in json.loads(kvsubst_list):
        namespace = i.get('namespace', '')
        key = i.get('key', None)
        value = i.get('value', None)
        if key is not None and value is not None:
            try:
                kvsubst_dict[namespace][key] = value
            except KeyError:
                kvsubst_dict[namespace] = {}
                kvsubst_dict[namespace][key] = value
    return kvsubst_dict
