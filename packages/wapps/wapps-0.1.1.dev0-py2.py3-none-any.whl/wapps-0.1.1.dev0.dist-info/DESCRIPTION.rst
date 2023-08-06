WApps
=====

`![CircleCI <https://img.shields.io/circleci/project/github/apihackers/wapps.svg>`_](https://circleci.com/gh/apihackers/workflows/wapps)
`![codecov <https://codecov.io/gh/apihackers/wapps/branch/master/graph/badge.svg>`_](https://codecov.io/gh/apihackers/wapps/branch/master)
`![Last version <https://img.shields.io/pypi/v/wapps.svg>`_](https://pypi.python.org/pypi/wapps)
`![License <https://img.shields.io/pypi/l/wapps.svg>`_](https://pypi.python.org/pypi/wapps)
`![Supported Python versions <https://img.shields.io/pypi/pyversions/wapps.svg>`_](https://pypi.python.org/pypi/wapps)

A very optionated set of Wagtail reusable applications and helpers
meant to speedup website development. There is not any universality intent.

stack
-----

It assumes the following stacks:

Server-side stack:
******************

- Python 3
- Latest Wagtail and Django versions
- Django-Jinja for template rendering
- Django-Babel for localization
- Django-Appconf for default settings

Frontend Stack
**************

- Vue 2 for front components
- Webpack 2 as front build toolchain
- SCSS as style language
- Bootstrap and Font-awesome as base frameworks

Requirements
------------

Wapps is designed to work with Python 3, Django-jinja, Django-babel and latest Django and Wagtail versions.

Wapps also provides JS/Vue2 helpers and scss mixins and classes

Installation
------------

Python installation
*******************

Install it with pip:

.. code-block:: shell

    $ pip install wapps



then add the required bases apps to your settings (ie. `settings.py`):

.. code-block:: python

    INSTALLED_APPS = [
        '...',
        'wapps',
        'memoize'
    ]



Node modules installation
*************************

Install it with `npm` or `yarn`

.. code-block:: shell

    $ npm install wapps@<wapps-version>



Changelog
=========

Current
-------

- Initial release



