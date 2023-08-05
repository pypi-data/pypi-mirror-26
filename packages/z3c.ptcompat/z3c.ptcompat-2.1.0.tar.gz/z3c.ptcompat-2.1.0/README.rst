Overview
========

.. image:: https://img.shields.io/pypi/v/z3c.ptcompat.svg
        :target: https://pypi.python.org/pypi/z3c.ptcompat/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/z3c.ptcompat.svg
        :target: https://pypi.org/project/z3c.ptcompat/
        :alt: Supported Python versions

.. image:: https://travis-ci.org/zopefoundation/z3c.ptcompat.svg?branch=master
        :target: https://travis-ci.org/zopefoundation/z3c.ptcompat

.. image:: https://coveralls.io/repos/github/zopefoundation/z3c.ptcompat/badge.svg?branch=master
        :target: https://coveralls.io/github/zopefoundation/z3c.ptcompat?branch=master

This package provides a page template engine implementation based on
Chameleon. It plugs into the `zope.pagetemplate
<https://pypi.python.org/pypi/zope.pagetemplate>`_ package and has an
explicit dependency on this package.

You can use the package to replace Zope's reference template engine
with Chameleon in an application based on the Zope Toolkit.

Configuration
-------------

The package is configured via ZCML.
