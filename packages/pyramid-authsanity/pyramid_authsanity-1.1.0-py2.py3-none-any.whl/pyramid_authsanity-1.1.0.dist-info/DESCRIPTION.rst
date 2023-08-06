==================
pyramid_authsanity
==================

An auth policy for the `Pyramid Web Framework
<https://trypyramid.com>`_ with sane defaults that works with `Michael
Merickel's <http://michael.merickel.org>`_ absolutely fantastic
`pyramid_services <https://github.com/mmerickel/pyramid_services>`_.
Provides an easy to use authorization policy that incorporates web security
best practices.

Installation
============

Install from `PyPI <https://pypi.python.org/pypi/pyramid_authsanity>`_ using
``pip`` or ``easy_install`` inside a virtual environment.

::

  $ $VENV/bin/pip install pyramid_authsanity

Or install directly from source.

::

  $ git clone https://github.com/usingnamespace/pyramid_authsanity.git
  $ cd pyramid_authsanity
  $ $VENV/bin/pip install -e .

Setup
=====

Activate ``pyramid_authsanity`` by including it into your pyramid application.

::

  config.include('pyramid_authsanity')



1.1.0 (2017-11-29)
==================

- Add new Authorization header based authentication source

  This provides out of the box support for "Bearer" like tokens.

1.0.0 (2017-05-19)
==================

- Remove Python 2.6 support

- Fix a bug whereby the policy was storing a dict instead of a list in the
  source, which of course broke things subtly when actually using the policy.

- Send empty cookie when forgetting the authentication for the cookie source


