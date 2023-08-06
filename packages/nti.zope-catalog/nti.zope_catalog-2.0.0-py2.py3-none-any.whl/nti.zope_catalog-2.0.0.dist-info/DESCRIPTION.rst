=================
 nti.zope_catalog
=================

.. image:: https://img.shields.io/pypi/v/nti.zope_catalog.svg
        :target: https://pypi.python.org/pypi/nti.zope_catalog/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/nti.zope_catalog.svg
        :target: https://pypi.org/project/nti.zope_catalog/
        :alt: Supported Python versions

.. image:: https://travis-ci.org/NextThought/nti.zope_catalog.svg?branch=master
        :target: https://travis-ci.org/NextThought/nti.zope_catalog

.. image:: https://coveralls.io/repos/github/NextThought/nti.zope_catalog/badge.svg?branch=master
        :target: https://coveralls.io/github/NextThought/nti.zope_catalog?branch=master

.. image:: https://readthedocs.org/projects/ntizope-catalog/badge/?version=latest
        :target: http://ntizope-catalog.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

Utilities and extensions for ZODB-based Zope catalogs and indexes.

This builds on both zope.catalog and zc.catalog.


=========
 Changes
=========

2.0.0 (2017-11-05)
==================

- Rename ``TimestampToNormalized64BitIntNormalizer`` to
  ``TimestampTo64BitIntNormalizer`` for consistency.
- Make ``TimestampTo64BitIntNormalizer`` subclass
  ``TimestampNormalizer`` for simplicity.
- Rename ``FloatToNormalized64BitIntNormalizer`` to
  ``PersistentFloatTo64BitIntNormalizer`` for consistency and to
  reflect its purpose.
- Make ``PersistentFloatTo64BitIntNormalizer`` subclass
  ``FloatTo64BitIntNormalizer``.
- Add ``IDeferredCatalog`` and an implementation in
  ``DeferredCatalog`` to allow creating catalog objects that don't
  participate in event subscription-based indexing. This replaces
  ``IMetadataIndex``, which is now an alias for this object. See
  `issue 3 <https://github.com/NextThought/nti.zope_catalog/pull/3>`_.

1.0.0 (2017-06-15)
==================

- First PyPI release.
- Add support for Python 3.
- ``TimestampNormalizer`` also normalizes incoming datetime objects.
- Fix extent-based queries for NormalizedKeywordIndex.
- 100% test coverage.


