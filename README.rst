.. image:: https://travis-ci.org/ome/omero-mapr.svg?branch=master
    :target: https://travis-ci.org/ome/omero-mapr

.. image:: https://badge.fury.io/py/omero-mapr.svg
    :target: https://badge.fury.io/py/omero-mapr


MAPR
====

OMERO.mapr is an OMERO.web app that enables browsing of data through attributes linked to images
in the form of Map Annotations.

It is used extensively by the `Image Data Resource <https://idr.openmicroscopy.org/>`_,
allowing users to find data by various categories such as Genes, Phenotypes, Organism etc.

In OMERO, Map Annotations are lists of named attributes or "Key-Value Pairs" that can be used to
annotate many types of data. Annotations can be assigned a ``namespace``
to indicate the origin and purpose of the annotation.

Map Annotations created by users via the Insight client or webclient all have the
namespace ``openmicroscopy.org/omero/client/mapAnnotation``, whereas other
Map Annotations created via the OMERO API by other tools should have their own distinct
namespace.

We can configure OMERO.mapr to search for Map Annotations of specified ``namespace``,
looking for ``Values`` under specifed ``Keys``.
For example, seach for values under key ``Gene Symbol`` or ``Gene Identifier``
and namespace ``openmicroscopy.org/mapr/gene``.

.. image:: https://user-images.githubusercontent.com/900055/36256919-d8a19fb6-124c-11e8-8628-d792ff29bd22.png


Requirements
============

* OMERO.web 5.6 or newer.

Installing from Pypi
====================

This section assumes that an OMERO.web is already installed.
NB: Configuration of the settings (see below) is not optional
and is required for the app to work.

Install the app using `pip <https://pip.pypa.io/en/stable/>`_:

::

    $ pip install omero-mapr

Add the app to the list of installed apps:

::

    $ bin/omero config append omero.web.apps '"omero_mapr"'


Config Settings
===============

You need to configure the namespaces and keys that you want users to be able to search for.

User-edited Map Annotations
---------------------------

Map Annotations that are added using the webclient or Insight in the Key-Value panel
use a specific "client" namespace. We can therefore configure OMERO.mapr to search
for these annotations using the namespace ``openmicroscopy.org/omero/client/mapAnnotation``.
For example, to search for "Primary Antibody" or "Secondary Antibody" values, we can add:

::

    $ bin/omero config append omero.web.mapr.config '{"menu": "antibody", "config":{"default":["Primary Antibody"], "all":["Primary Antibody", "Secondary Antibody"], "ns":["openmicroscopy.org/omero/client/mapAnnotation"], "label":"Antibody"}}'

We can add an "Antibodies" link to the top of the webclient page to take us to the Antibodies search page.
The link tooltip is "Find Antibody values".
The ``viewname`` should be in the form ``maprindex_{menu}`` where ``{menu}`` is the the ``menu`` value in the previous config.

::

    $ bin/omero config append omero.web.ui.top_links '["Antibodies", {"viewname": "maprindex_antibody"}, {"title": "Find Antibody values"}]'

After restarting web, we can now search for Antibodies:

.. image:: https://user-images.githubusercontent.com/900055/40605069-063ff29a-6259-11e8-9295-3887dde0441f.png


We can also specify an empty list of keys to search for *any* value.

::

    $ bin/omero config append omero.web.mapr.config '{"menu": "anyvalue", "config":{"default":["Any Value"], "all":[], "ns":["openmicroscopy.org/omero/client/mapAnnotation"], "label":"Any"}}'

    # Top link
    $ bin/omero config append omero.web.ui.top_links '["Any Value", {"viewname": "maprindex_anyvalue"}, {"title": "Find Any Value"}]'

After restarting web, we can now search for any Value, such as "INCENP":

.. image:: https://user-images.githubusercontent.com/900055/40605101-1cd1925c-6259-11e8-93a8-e72af2e570d3.png


Other Map Annotations
---------------------

In this example we want to search
for Map Annotations of namespace ``openmicroscopy.org/mapr/gene`` searching for
attributes under the ``Gene Symbol`` and ``Gene Identifier`` keys.

::

    $ bin/omero config append omero.web.mapr.config '{"menu": "gene","config": {"default": ["Gene Symbol"],"all": ["Gene Symbol", "Gene Identifier"],"ns": ["openmicroscopy.org/mapr/gene"],"label": "Gene"}}'

Now add a top link of ``Genes`` with tooltip ``Find Gene annotations`` that will take us to the ``gene`` search page. The ``query_string`` parameters are added to the URL, with ``"experimenter": -1``
specifying that we want to search across all users.

::

    $ bin/omero config append omero.web.ui.top_links '["Genes", {"viewname": "maprindex_gene", "query_string": {"experimenter": -1}}, {"title": "Find Gene annotations"}]'


Finally, we can add a map annotation to an Image that is in a Screen -> Plate -> Well
or Project -> Dataset -> Image hierarchy.
This code uses the OMERO `Python API <https://docs.openmicroscopy.org/latest/omero/developers/Python.html>`_ to
add a map annotation corresponding to the configuration above:

::

    key_value_data = [["Gene Identifier","ENSG00000117399"],
                      ["Gene Identifier URL", "http://www.ensembl.org/id/ENSG00000117399"],
                      ["Gene Symbol","CDC20"]]
    map_ann = omero.gateway.MapAnnotationWrapper(conn)
    map_ann.setValue(key_value_data)
    map_ann.setNs("openmicroscopy.org/mapr/gene")
    map_ann.save()
    image = conn.getObject('Image', 2917)
    image.linkAnnotation(map_ann)


Now restart OMERO.web as normal for the configuration above to take effect.
You should now be able to browse to a ``Genes`` page and search for
``CDC20`` or ``ENSG00000117399``.


Value substitutions
-------------------

Mapr can automatically post-process values based on matching keys.
This can be useful for cross-referencing public identifiers.
``omero.web.mapr.metadata_kv_substitutions`` is a list of dictionaries with the following required fields:

* ``namespace``: Only apply to key-value pairs in this namespace
* ``key``: The key name to match
* ``value``: The replacement template value, all instances of ``{{value}}`` will be replaced with the original value.

For example, this will convert all values in namespace ``idr.openmicroscopy.org/study/info`` to PubMed URLs where the key is ``PubMed ID`` and the value is the PubMed Identifier::

    $ bin/omero config set -- omero.web.mapr.metadata_kv_substitutions '[{"namespace": "idr.openmicroscopy.org/study/info", "key": "PubMed ID", "value": "<a href=\"https://www.ncbi.nlm.nih.gov/pubmed/{{value}}\">{{value}}</a>"}]'


Testing
=======

Testing MAPR requires OMERO.server running.
Run tests (includes self-contained OMERO.server, requires docker)::

    docker-compose -f docker/docker-compose.yml up --build --abort-on-container-exit
    docker-compose -f docker/docker-compose.yml rm -fv

License
-------

MAPR is released under the AGPL.


Copyright
---------

2016-2020, The Open Microscopy Environment
