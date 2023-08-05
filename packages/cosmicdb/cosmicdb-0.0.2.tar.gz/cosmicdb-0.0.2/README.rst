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

1. Add ``cosmicdb`` and requirements to your INSTALLED_APPS setting like this::

        INSTALLED_APPS = (
            ...
            'django.contrib.sites',
            'cosmicdb',
            'dal',
            'dal_select2',
            'crispy_forms',
            'django_tables2',
        )

2. Add ``cosmicdb.urls`` to your urls.py like this::

        urlpatterns = [
            ...
            url(r'^', include('cosmicdb.urls')),
        ]

3. Add cosmicdb settings like this::

        COSMICDB_SITE_TITLE = 'My Site'
        AUTH_USER_MODEL = 'cosmicdb.User'
        LOGIN_URL = '/login/'
        CRISPY_TEMPLATE_PACK = 'bootstrap3'
        DJANGO_TABLES2_TEMPLATE = 'django_tables2/bootstrap-responsive.html'

4. Run ``python manage.py migrate``

5. Run ``python manage.py collectstatic``

Requirements
============

`Django>=1.11
<https://github.com/django/django/>`_