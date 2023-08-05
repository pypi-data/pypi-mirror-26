==========================
CosmicDB Django App
==========================

Install
=======

- Run ``virtualenv demoenv --no-site-packages``
- Run ``demoenv\Scripts\activate``
- Run ``pip install Django``
- Run ``pip install -e git+davidbradleycole@bitbucket.org:davidbradleycole/cosmicdb.git``


Usage
=====

1. Add ``cosmicdb`` to your INSTALLED_APPS setting like this::

       INSTALLED_APPS = (
           ...
           'cosmicdb',
       )

2. Run ``python manage.py migrate``

Requirements
============

`Django>=1.11
<https://github.com/django/django/>`_

