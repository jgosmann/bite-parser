Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[0.1.1] - 2022-01-30
--------------------

Added
^^^^^

* ``Group`` transform to introduce explicit groupings, now that parse values
  are flattened otherwise (see below).
* ``Not`` parser to allow for negative look-ahead.
* ``Forward`` declaration parser to allow for recursive rules.
* ``BytesBuffer`` and ``parse_bytes`` for easier usage without asyncio streams.

Changed
^^^^^^^

* Renamed the ``value`` property of ``ParseNode`` to ``values``. All nodes
  return now iterables and sub-values will be flattened into a common iterable.
* Renamed ``TransformValue`` to ``TransformValue`` as it now gets and is
  expected to produce an iterable of values.
* ``Opt`` has no longer a custom implementation, but is just equivalent to
  ``expr[0, 1]``.

Removed
^^^^^^^

* ``OnlyValue``


Fixed
^^^^^

* Fixed detection of EOF in streams to prevent ``parse_incremental`` from
  raising unexpected parse errors. The ``MockReader`` is now more closely
  matching the EOF behavior of ``StreamReader``.
* Fixed off-by-one error which could lead to a stalling reader waiting for a
  byte that never will be sent.


[0.1.0] - 2022-01-29
--------------------

Initial release.
