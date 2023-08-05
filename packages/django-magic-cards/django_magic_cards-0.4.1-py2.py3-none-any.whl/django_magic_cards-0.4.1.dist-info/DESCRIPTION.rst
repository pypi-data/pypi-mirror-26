==================
Django Magic Cards
==================

.. image:: https://badge.fury.io/py/django-magic-cards.svg
    :target: https://badge.fury.io/py/django-magic-cards

.. image:: https://travis-ci.org/pbaranay/django-magic-cards.svg?branch=master
    :target: https://travis-ci.org/pbaranay/django-magic-cards

.. image:: https://codecov.io/gh/pbaranay/django-magic-cards/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/pbaranay/django-magic-cards

Django Magic Cards is a pluggable Django app for the Oracle text of all Magic: the Gathering cards.

Documentation
-------------

The full documentation is at https://django-magic-cards.readthedocs.io.

Quickstart
----------

Install the package::

    pip install django-magic-cards

Add the app to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'magic_cards.apps.MagicCardsConfig',
        ...
    )

Add Django Magic Cards' tables to your the database::

    ./manage.py migrate magic_cards

Populate the card database::

    ./manage.py import_magic_cards

Acknowledgments
---------------

* MTGJSON_ for providing up-to-date card data.
* Cookiecutter_ and `cookiecutter-djangopackage`_ for providing the structure for this project.

.. _MTGJSON: http://mtgjson.com/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage

Disclaimer
----------

The literal and graphical information presented in this software about Magic: the Gathering, including Oracle text and card images, is copyright Wizards of the Coast, LLC, a subsidiary of Hasbro, Inc. This project is not produced by, endorsed by, supported by, or affiliated with Wizards of the Coast.




History
-------

0.4.1 (2017-10-26)
++++++++++++++++++

* Improve Unicode handling on Python 2, allowing the Printings admin
  page to load properly (`#27`_).

.. _#27: https://github.com/pbaranay/django-magic-cards/issues/27

0.4.0 (2017-10-04)
++++++++++++++++++

* Update a `Card`'s data (text, loyalty, types, etc.) when a set is re-imported (`#23`_).

.. _#23: https://github.com/pbaranay/django-magic-cards/issues/23

0.3.0 (2017-09-28)
++++++++++++++++++

* Store planeswalkers' starting loyalty (`#19`_).
* Correctly populate flavor text.
* Fix issue that crashed re-importing a set without multiverse IDs.

.. _#19: https://github.com/pbaranay/django-magic-cards/issues/19

0.2.0 (2017-08-16)
++++++++++++++++++

* Speed up import function (`#9`_).
* Implement basic admin pages (`#7`_).

.. _#9: https://github.com/pbaranay/django-magic-cards/issues/9
.. _#7: https://github.com/pbaranay/django-magic-cards/issues/7

0.1.1 (2017-08-10)
++++++++++++++++++

* Increase maximum length of a `Card`'s `name` (`#2`_).

.. _#2: https://github.com/pbaranay/django-magic-cards/issues/2

0.1.0 (2017-08-08)
++++++++++++++++++

* First release on PyPI.


