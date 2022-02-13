from asyncio import StreamReader
from typing import AsyncGenerator, TypeVar

from bite.io import BytesBuffer, StreamReaderBuffer
from bite.parsers import ParsedNode, Parser, TrailingBytesError

T = TypeVar("T", covariant=True)
V = TypeVar("V", covariant=True)


async def parse_incremental(
    grammar: Parser[T, V], reader: StreamReader
) -> AsyncGenerator[ParsedNode[T, V], None]:
    r"""Parse bytes from an asynchronous stream incrementally.

    Parameters
    ----------
    grammar:
        Parser combinators defining the grammar to parse.
    reader:
        The stream reader to read bytes with.

    Yields
    ------
    :
        A parse tree for each complete match of the given *grammar*. Note that
        location indices of the parse tree will be relative to the start of that
        parsed segment.

    Raises
    ------
    bite.parsers.ParseError
        If the provided *grammar* fails to parse the incoming bytes.

    Examples
    --------

    .. testcode:: parse_incremental

        import asyncio
        from bite import CharacterSet, Combine, Literal, parse_incremental, Suppress

        integer_token = Combine(CharacterSet(b'0123456789')[1, ...])
        line = integer_token + Literal(b'+') + integer_token + Suppress(Literal(b'\r\n'))

        async def open_reader():
            # For example:
            # reader, _ = await asyncio.open_connection(...)
            # return reader
            ...

    .. testcode:: parse_incremental
        :hide:

        from bite.tests.mock_reader import MockReader

        async def open_reader():
            return MockReader(b"1+2\r\n23+42\r\n1234+4321\r\n")

    .. testcode:: parse_incremental

        async def main():
            reader = await open_reader()
            async for parsed_line in parse_incremental(line, reader):
                print("Parsed line:", parsed_line.values)

        asyncio.run(main())

    Assuming the bytes ``b"1+2\r\n23+42\r\n1234+4321\r\n"`` can be read from
    the *reader*:

    .. testoutput:: parse_incremental

        Parsed line: (b'1', b'+', b'2')
        Parsed line: (b'23', b'+', b'42')
        Parsed line: (b'1234', b'+', b'4321')
    """

    buffer = StreamReaderBuffer(reader)
    while not buffer.at_eof():
        parse_tree = await grammar.parse(buffer, 0)
        yield parse_tree
        await buffer.drop_prefix(parse_tree.end_loc)
        await buffer.get(slice(0, 1))  # Ensure to read EOF state


async def parse_bytes(
    grammar: Parser[T, V], data: bytes, *, parse_all: bool = False
) -> ParsedNode[T, V]:
    """Parse an in-memory bytes object.

    Parameters
    ----------
    grammar:
        Parser combinators defining the grammar to parse.
    data:
        The bytes object to parse.
    parse_all:
        If set to ``True``, the all bytes must be parsed. Otherwise, trailing,
        unparsed bytes are allowed.

    Returns
    -------
    The resulting parse tree.

    Exceptions
    ----------
    bite.parsers.TrailingBytesError
        If ``parse_all=True`` and not all input was consumed by the parser.
    bite.parsers.ParseError
        If the provided *grammar* fails to parse the incoming bytes.

    Examples
    --------
    .. testcode:: parse_bytes

        import asyncio
        from bite import Literal, parse_bytes

        print(asyncio.run(parse_bytes(Literal(b'A'), b'AB')).values)

    .. testoutput:: parse_bytes

        (b'A',)

    .. testcode:: parse_bytes

        asyncio.run(parse_bytes(Literal(b'A'), b'AB', parse_all=True))

    .. testoutput:: parse_bytes

        Traceback (most recent call last):
            ...
        bite.parsers.TrailingBytesError: trailing bytes
    """

    parse_tree = await grammar.parse(BytesBuffer(data))
    if parse_all and parse_tree.end_loc < len(data):
        raise TrailingBytesError("trailing bytes")
    return parse_tree
