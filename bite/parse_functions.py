from asyncio import StreamReader
from typing import AsyncGenerator, TypeVar

from bite.io import BytesBuffer, StreamReaderBuffer
from bite.parsers import ParsedNode, Parser, TrailingBytesError

T = TypeVar("T", covariant=True)
V = TypeVar("V", covariant=True)


async def parse_incremental(
    grammar: Parser[T, V], reader: StreamReader
) -> AsyncGenerator[ParsedNode[T, V], None]:
    buffer = StreamReaderBuffer(reader)
    while not buffer.at_eof():
        parse_tree = await grammar.parse(buffer, 0)
        yield parse_tree
        await buffer.drop_prefix(parse_tree.end_loc)
        await buffer.get(slice(0, 1))  # Ensure to read EOF state


async def parse_bytes(
    grammar: Parser[T, V], data: bytes, *, parse_all: bool = False
) -> ParsedNode[T, V]:
    parse_tree = await grammar.parse(BytesBuffer(data))
    if parse_all and parse_tree.end_loc < len(data):
        raise TrailingBytesError("trailing bytes")
    return parse_tree
