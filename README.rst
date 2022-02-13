.. image:: https://github.com/jgosmann/bite-parser/actions/workflows/ci.yml/badge.svg
  :target: https://github.com/jgosmann/bite-parser/actions/workflows/ci.yml
  :alt: CI and release pipeline
.. image:: https://codecov.io/gh/jgosmann/bite-parser/branch/main/graph/badge.svg?token=O4M05YWNQK
  :target: https://codecov.io/gh/jgosmann/bite-parser
  :alt: Codecov coverage
.. image:: https://img.shields.io/pypi/v/bite-parser
  :target: https://pypi.org/project/bite-parser/
  :alt: PyPI
.. image:: https://img.shields.io/pypi/pyversions/bite-parser
  :target: https://pypi.org/project/bite-parser/
  :alt: PyPI - Python Version
.. image:: https://img.shields.io/pypi/l/bite-parser
  :target: https://pypi.org/project/bite-parser/
  :alt: PyPI - License

Welcome to bite-parser
======================

   Asynchronous parser taking incremental bites out of your byte input stream.

The bite-parser is a parser combinator library for Python.
It is similar to `PyParsing <https://github.com/pyparsing/pyparsing>`_
in that it allows the construction of grammars for parsing
from simple building blocks in pure Python.
This approach is also known as `Parsing Expression Grammar (PEG)
<https://en.wikipedia.org/wiki/Parsing_expression_grammar>`_.
While PyParsing
(and many other Python parsing libraries)
only support string,
bite-parser operates on bytes.
In addition,
bite-parser makes use of `asyncio`
and can asynchronously generate parsed items
from an input stream.

A typical use-case would be the parsing of a network protocol
like IMAP.
In fact,
I wrote this library for the IMAP implementation of my
`dmarc-metrics-exporter <https://github.com/jgosmann/dmarc-metrics-exporter>`_.

.. note::
   I have implemented the fundamental set of parsers,
   which should allow constructing most or all grammars
   recognizable by this type of parser.
   However, many convenience or higher level parsers are not yet implemented.

   Other areas that still need improvement are:

   * Abilitiy to debug the parsing.
   * Better error messages.
   * Performance: Currently, only a basic recursive descent parser is
     implemented which can exhibit exponential worst case performance.
     This could be improved by implementing a packrat parser.

Important links
---------------

* `Documentation <https://jgosmann.github.io/bite-parser/docs/en/main/>`_
* `GitHub repository <https://github.com/jgosmann/bite-parser>`_
