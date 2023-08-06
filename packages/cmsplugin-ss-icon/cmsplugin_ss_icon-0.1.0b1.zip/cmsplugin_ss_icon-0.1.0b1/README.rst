.. image:: https://travis-ci.org/alexjbartlett/djangocms-ss-icon.svg?branch=master
    :target: https://travis-ci.org/alexjbartlett/djangocms-ss-icon

djangocms font-awesome icon plugin
==================================

A simple plugin for djangocms that renders a font awesome icon using a <i> tag.

Installation
------------

    pip install cmsplugin_ss_icon

In your settings.py

    INSTALLED_APPS = (
        ...
        'cmsplugin_ss_icon',
    )

This package assumes that font-awesome css and fonts are already available in your build.  For information
about how to include font-awesome on your site see the official documentation_.

.. _documentation: http://fontawesome.io/get-started/

Tested on
    * Python 2.7. 3.4, 3.5
    * Django 1.8, 1.9, 1.10
    * DjangoCms 3.4
