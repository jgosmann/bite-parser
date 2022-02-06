.. bite-parser documentation master file, created by
   sphinx-quickstart on Tue Feb  1 19:20:07 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to bite-parser's documentation!
=======================================

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


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started
   api/api
   changelog
   license



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
