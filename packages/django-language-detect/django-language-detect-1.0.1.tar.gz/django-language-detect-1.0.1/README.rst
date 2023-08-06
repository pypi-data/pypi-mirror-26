======================
django-language-detect
======================

Installation
============

::

    pip install django-language-detect


Usage
=====


::
    

    request.browser_language


Settings.py
===========

::

    # Use `MIDDLEWARE_CLASSES` prior to Django 1.10
    MIDDLEWARE = (
        ...
        'language_detect.middleware.BrowserLanguageDetectionMiddleware',
        ...
    )
