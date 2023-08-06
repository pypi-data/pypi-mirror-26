=============================
Django Chaos Tickets
=============================

.. image:: https://badge.fury.io/py/django-chaos-tickets.svg
    :target: https://badge.fury.io/py/django-chaos-tickets

.. image:: https://travis-ci.org/george-silva/django-chaos-tickets.svg?branch=master
    :target: https://travis-ci.org/george-silva/django-chaos-tickets

.. image:: https://codecov.io/gh/george-silva/django-chaos-tickets/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/george-silva/django-chaos-tickets

Ticketing system from Django and Django Chaos

Documentation
-------------

The full documentation is at https://django-chaos-tickets.readthedocs.io.

Quickstart
----------

Install Django Chaos Tickets::

    pip install django-chaos-tickets

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'chaos_tickets.apps.ChaosTicketsConfig',
        ...
    )

Add Django Chaos Tickets's URL patterns:

.. code-block:: python

    from chaos_tickets import urls as chaos_tickets_urls


    urlpatterns = [
        ...
        url(r'^', include(chaos_tickets_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
