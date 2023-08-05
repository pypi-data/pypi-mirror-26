==========================
CosmicDB Django App
==========================

Install
=======

- Run ``virtualenv demoenv --no-site-packages``
- Run ``demoenv\Scripts\activate``
- Run ``pip install Django``
- Run ``django-admin startproject demo``
- Run ``pip install cosmicdb``


Usage
=====

1. Add ``cosmicdb`` and requirements to your INSTALLED_APPS setting like this::

        INSTALLED_APPS = (
            'cosmicdb',
            'dal',
            'dal_select2',
            'crispy_forms',
            'django_tables2',
            ...
        )

2. Add ``cosmicdb.urls`` to your urls.py like this::

        from django.conf.urls import url, include

        urlpatterns = [
            ...
            url(r'^', include('cosmicdb.urls')),
        ]

3. Add cosmicdb settings to your settings.py like this::

        COSMICDB_SITE_TITLE = 'Demo Site'
        COSMICDB_ALLOW_SIGNUP = False
        AUTH_USER_MODEL = 'cosmicdb.User'
        LOGIN_URL = '/login/'
        CRISPY_TEMPLATE_PACK = 'bootstrap3'
        DJANGO_TABLES2_TEMPLATE = 'django_tables2/bootstrap-responsive.html'
        EMAIL_USE_TLS = True
        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_PORT = 587
        EMAIL_HOST_USER = 'test@test.com'
        EMAIL_HOST_PASSWORD = 'testpassword'
        DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
        DEFAULT_FROM_EMAIL_NAME = COSMICDB_SITE_TITLE


4. Run ``python manage.py migrate``

5. Run ``python manage.py collectstatic``

6. Run ``python manage.py createsuperuser``

Requirements
============

`Django>=1.11
<https://github.com/django/django/>`_


Dev Notes
=========
``python setup.py sdist bdist_wheel``
``twine upload dist/0.0.1*``


