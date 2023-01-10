API reference
=============


.. currentmodule:: bite

Parsing functions
-----------------

These functions are intended as the main entry points to parsing something
with a grammar defined with the `Parser combinators`_. All parsing functions
can also be directly imported from the ``bite`` package.

.. autosummary::

    parse_functions.parse_bytes
    parse_functions.parse_incremental


Parser combinators
------------------

These classes can be combined to create the desired parser for a given grammar.
All parser combinators can also be directly imported from the ``bite`` package.


Parsing concrete bytes
^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :nosignatures:

    parsers.CaselessLiteral
    parsers.CharacterSet
    parsers.FixedByteCount
    parsers.Literal

Combining parsers
^^^^^^^^^^^^^^^^^

Parser instances can also be combined with the following operators:

    - ``+`` (:class:`And`): Apply parsers in sequence.
    - ``|`` (:class:`MatchFirst`): Apply the first parser that succeeds parsing
      the input.
    - ``~`` (:class:`Not`): Negative look-ahead.

.. autosummary::
   :nosignatures:

   parsers.And
   parsers.Combine
   parsers.Forward
   parsers.MatchFirst
   parsers.Not

Repetition of parsers
^^^^^^^^^^^^^^^^^^^^^

Repetition of a parser instance can also be declared with indexing/bracket
notation as ``parser[x, y]``. `` x`` must be a non-negative integer. ``y`` must
be either a positive integer or the ellipsis ``...`` to allow for unlimited
repetitions.

.. autosummary::
   :nosignatures:

    parsers.Counted
    parsers.OneOrMore
    parsers.Opt
    parsers.Repeat
    parsers.ZeroOrMore

Transforming parsed values
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :nosignatures:

    transformers.Group
    transformers.Suppress
    transformers.Transform
    transformers.TransformValues


Parse tree nodes
----------------

These classes define the structure of the parse tree returned from a parser.
The general protocol of these classes is given by :class:`parsers.ParsedNode`.
Besides the fundamental class listed here, many parsers define their
specialized implemenations.

.. autosummary::
   :nosignatures:

     parsers.ParsedLeaf
     parsers.ParsedNil
     parsers.ParsedNode

Module reference
----------------

.. toctree::

   io
   parse_functions
   parsers
   tests
   transformers
