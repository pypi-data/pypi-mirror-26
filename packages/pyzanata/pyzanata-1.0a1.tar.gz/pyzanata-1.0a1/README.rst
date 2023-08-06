pyzanata
========

Alternative `Zanata <http://zanata.org/>`_ restapi client.

Usage
-----

In order to get started two imports are needed::

    from pyzanata import ZanataCredentials
    from pyzanata import ZanataClient

First credentials needs to be set::

    credentials = ZanataCredentials('http://zanata.exampl.com', 'johndoe', 'secret')

Then the client can be initialized::

    client = ZanataClient(credentials)

Now Zanata infos can be fetched (or set) like so::

    client.ProjectsResource.projects.GET()
    client.ProjectResource.project.GET(projectSlug='myproject')

It has always the form ``client.RESOURCE.ENDPOINT.METHOD(data=None, **path_replacements)``.

RESOURCE
    name of the resource according the the declaration (first level).

ENDPOINT
    name of the endpoint according the the declaration (second level).

METHOD
    one of the http-methods (depends on endpint, as configured in declaration)

data
    payload or body passed to ``requests`` call.

path_replacements
    keyword arguments used to replace the dynamic path elements as configured in the declaration.

Consult the `Zanata REST API Documentation <https://zanata.ci.cloudbees.com/job/zanata-api-site/site/zanata-common-api/rest-api-docs/index.html#resources>`_ for details. Deprecated APIs are not implemented.

See also the `Declaration YAML File (GitHub) <https://github.com/collective/pyzanata/blob/master/src/pyzanata/restapi.yaml>`_. This file is read by the generic API runtime code and declares the API.




Contribute
----------

- Issue Tracker: https://github.com/bluedynamics/pyzanata/issues
- Source Code: https://github.com/bluedynamics/pyzanata


Support
-------

If you are having issues, please let me know: jens@bluedynamics.com

