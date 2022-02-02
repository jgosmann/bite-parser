Getting Started
===============

Installation
------------

Run the following in your command line::

    pip install -U bite-parser


Implementing your first parser
------------------------------

.. testcode:: getting-started-0

    from bite import Combine, CharacterSet, Forward, Literal

    value = Forward()
    product = value + ((Literal(b'*') | Literal(b'/')) + value)[0, ...]
    sum = product + ((Literal(b'+') | Literal(b'-')) + product)[0, ...]
    expr = sum
    value.assign(
        Combine(CharacterSet(b'0123456789')[1, ...], name="number")
        | (Literal(b'(') + expr + Literal(b')'))
    )

This defines a grammar to accept simple mathematical expressions
consisting of the four basic operations.
Let us discuss the most basic elements first.
Each ``Literal`` defines a byte or sequence of bytes
that needs to be matched exactly.
The ``|`` (or) operator combines parsers
such that the first matching alternative determines the parse result.
Order can matter here
(but not in this example)!
The ``+`` (addition) operator chains parsers together,
i.e. first the left-hand side parser needs to match the input,
followed by a match of the right-hand parser.
The bracket notation declares the minimum and maximum number of repeats.
Zero or more matches are denoted by ``[0, ...]``,
one or more matches with ``[1, ...]``.

Further, the ``CharacterSet`` matches a single byte from the given set.
Because a number might have multiple digits,
``[1, ...]`` is used to allow for more than one digit.
However,
we do not want to parse each digit individually,
but combine all of the digits into a single token.
This is done with ``Combine``.

Finally, the ``Forward`` allows to do a forward declaration of ``value``
without specifying what constitutes a value
until ``value.assign`` is called.
This allows for the definition of recursive rules.
Be careful though, a left-recursive rule will give an infinite recursion!
You can add names such as "number" to declarations in your grammar.
This can come in handy when evaluating the parse result.

There many more classes and operators
that you can use to construct your grammar.
Check the reference documentation.
Also note,
that for each operator an equivalent class exists
that can be used interchangeably.


Using the parser
----------------

.. testcode:: getting-started-0

    import asyncio
    from bite import parse_bytes

    result = asyncio.run(parse_bytes(expr, b'123+45*(67+89)'))

Here the ``parse_bytes`` function is used
to parse the bytes ``b'123+45*(67+89)'``
with the ``expr`` grammar (or parser).
The result is the concrete parse tree
which contains all the relevant parsing information.
The children of each node will be stored in the ``parse_tree`` attribute.
For example,
we can take a look at the first child of ``result``
which corresponds to ``123`` from the parsed expression:

.. testcode:: getting-started-0

   print(result.parse_tree[0])

.. testoutput:: getting-started-0

    ParsedMatchFirst(name="(number) | ((b'(') + ((forward) + ((((b'*') | (b'/')) + (forward))[0, None]) + ((((b'+') | (b'-')) + ((forward) + ((((b'*') | (b'/')) + (forward))[0, None])))[0, None])) + (b')'))", parse_tree=ParsedLeaf(name='number', parse_tree=b'123', start_loc=0, end_loc=3), choice_index=0)

The ``ParsedMatchFirst`` corresponds to the ``|`` operator
of the rule assigned to ``value``.
It has also a somewhat unwieldy, auto-generated name
besides some other attributes.
On each node in the parse tree,
you can query ``start_loc`` and ``end_loc`` to find out to what extent in the input the parsed node corresponds.
The ``end_loc`` is exclusive.

.. testcode:: getting-started-0

    print(
        "Extent from", result.parse_tree[0].start_loc,
        "to", result.parse_tree[0].end_loc
    )

.. testoutput:: getting-started-0

    Extent from 0 to 3

The leaf nodes of the parse tree will have the bytes itself as ``parse_tree`` attribute:

.. testcode:: getting-started-0

    print("The leaf:", result.parse_tree[0].parse_tree)
    print(
        "The children of the leaf are the bytes itself:",
        result.parse_tree[0].parse_tree.parse_tree
    )

.. testoutput:: getting-started-0

    The leaf: ParsedLeaf(name='number', parse_tree=b'123', start_loc=0, end_loc=3)
    The children of the leaf are the bytes itself: b'123'

While the parse tree gives you all the information,
it is often more than you need and sometimes cumbersome to work with.
Often you only want a transformed representation
that you can get with the ``values`` attribute on a node.

.. testcode:: getting-started-0

    print(result.values)

.. testoutput:: getting-started-0

    (b'123', b'+', b'45', b'*', b'(', b'67', b'+', b'89', b')')

By default this gives a flat tuple of all the parsed tokens.
In the next section,
we will introduce some more structure to retain the operator precedence.


Introducing structure in the parse result
-----------------------------------------

A simple way to introduce more structure into the parse values is the ``Group``
transform.
It will put the values of its sub-parsers into a tuple.
In addition,
``Suppress`` allows to remove parsed tokens completely from the values.
In this example,
we use this to insert grouping according to the precedence.

.. testcode:: getting-started-1

    import asyncio
    from bite import Combine, CharacterSet, Forward, Group, Literal, Suppress
    from bite import parse_bytes

    value = Forward()
    product = Group(value + ((Literal(b'*') | Literal(b'/')) + value)[0, ...])
    sum = product + ((Literal(b'+') | Literal(b'-')) + product)[0, ...]
    expr = sum
    value.assign(
        Combine(CharacterSet(b'0123456789')[1, ...], name="number")
        | Group(Suppress(Literal(b'(')) + expr + Suppress(Literal(b')')))
    )

    result = asyncio.run(parse_bytes(expr, b'123+45*(67+89)'))

    print(result.values)

.. testoutput:: getting-started-1

    ((b'123',), b'+', (b'45', b'*', ((b'67',), b'+', (b'89',))))

It is also possible to define custom transforms
and use this,
for example,
to evaluate the whole expression.

.. testcode:: getting-started-1

    import asyncio
    from bite import Combine, CharacterSet, Forward, Literal, Suppress, TransformValues
    from bite import parse_bytes

    def eval_product(values):
        acc = values[0]
        for i in range(1, len(values), 2):
            if values[i] == b'*':
                acc *= values[i + 1]
            elif values[i] == b'/':
                acc /= values[i + 1]
            else:
                raise ValueError()
        return (acc,)

    def eval_sum(values):
        acc = values[0]
        for i in range(1, len(values), 2):
            if values[i] == b'+':
                acc += values[i + 1]
            elif values[i] == b'-':
                acc -= values[i + 1]
            else:
                raise ValueError()
        return (acc,)

    value = Forward()
    product = TransformValues(
        value + ((Literal(b'*') | Literal(b'/')) + value)[0, ...],
        eval_product
    )
    sum = TransformValues(
        product + ((Literal(b'+') | Literal(b'-')) + product)[0, ...],
        eval_sum
    )
    expr = sum
    value.assign(
        TransformValues(
            Combine(CharacterSet(b'0123456789')[1, ...], name="number"),
            lambda values: (int(v) for v in values)
        )
        | Suppress(Literal(b'(')) + expr + Suppress(Literal(b')'))
    )

    result = asyncio.run(parse_bytes(expr, b'123+45*(67+89)'))

    print(result.values)

.. testoutput:: getting-started-1

    (7143,)


Parsing asynchronous streams
----------------------------

So far we only parsed complete byte arrays.
However, bite-parser is asynchronous
and can emit parsed results as they come in.
For this the ``parse_incremental`` method is used.
It returns an asynchronous iterator
that returns each successive complete parse tree.

The following example implements a simple server
that parses and evaluates each incoming line
with the grammar defined in the previous section.

.. testcode:: getting-started-1

    from bite import Opt

    request = expr + Opt(Literal(b'\r')) + Literal(b'\n')

    async def handle_connection(reader, writer):
        try:
            # The following line is where the magic happens
            async for result in parse_incremental(request, reader):
                writer.write(b'Result: ')
                writer.write(str(result.values[0]).encode('ascii'))
                writer.write(b'\n')
                await writer.drain()
        finally:
            writer.write_eof()
            await writer.drain()
            writer.close()

    async def main():
        server = await asyncio.start_server(handle_connection, 'localhost', 4000)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()

    if __name__ == '__main__':
        asyncio.run(main())

After starting the server,
you can test the server with netcat (for example):

.. code-block:: bash

    nc localhost 4000

.. code-block::

    1+1
    Result: 2
    21+4*(5+6)-4/2
    Result: 63.0
