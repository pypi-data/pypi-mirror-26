Django Data Explorer facilitates visualizing data using AJAX tables and maps
 with filters in Django applications.

You can see the examples at [http://djangoqb.qed.ai/](http://djangoqb.qed.ai/).

Previously this project was released under name `django-querybuilder`

Running examples
================

You can see example Django project using Django Data Explorer in directory
`example`. Go to the directory and execute:

    pip install -r requirements.txt

And then:

    ./manage.py runserver


Using in your application
=========================

Add those lines to you project requirements or use them as PIP arguments.

    django-data-explorer
    -e git+git://github.com/qedsoftware/django-datatable-view#egg=django-datatable-view   # for data-explorer

Afterwards, you can use our package the same way as in the example. You can
 also consult docstrings.

For developers
==============

Frontend requirements
---------------------

To get frontend dependencies, you need to have `Node.js` installed.

After installing `Node.js`, install the frontend dependencies by running
the following from the root of your Django checkout:

    npm install
    npm run deps

Then build frontend files:

    npm run build

For development run

    npm run start

that way build will happen automatically each time you change any related files.

Django static files - important note
------------------------------------
Contents of the folders listed below are generated automatically.

    /django_data_explorer/static/django_data_explorer/dist
    /django_data_explorer/static/django_data_explorer/css
    /django_data_explorer/static/django_data_explorer/libs

Modifying them manually does not make much sense, as they will be overridden.

They are included to enable the package to work immediately after installing it via pip.

Documentation
-------------

In Python, see docstrings for documentation. You can also browse them using
`help` method and using:

    python -m pydoc django_data_explorer

Generate JavaScript docs into directory `js_docs`:

    npm run js-docs

Running tests
=============

Django
------

    ./manage.py jenkins

Frontend
--------

    npm test

All tests
--------
    ./jenkins.py

Test coverage
=============

JavaScript test coverage is available in the test output. To see Python coverage
report, execute in directory `example`:

    coverage3 run ./manage.py test
    coverage3 html ../django_data_explorer/*py
