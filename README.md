djtemplate
==========

A very opinionated template for a django project.

Complete with:

* html5boilerplate
* twitter bootstrap
* jQuery
* Backbone.js (Underscore.js)
* ... other useful javscript libraries
* ... some useful Django apps and patterns

To use:

    django-admin.py startproject --template=path/to/djtemplate myprojectname
    cd myprojectname
    virtualenv env
    source env/bin/activate
    pip install -e .
    psql -c 'create database myprojectname;'
    echo 'from myprojectname.conf.settings.dev import *' > settings_local.py
    echo '/env/\nsettings_local.py' > .gitignore
    git init
    ./manage.py syncdb
    ./manage.py runserver
