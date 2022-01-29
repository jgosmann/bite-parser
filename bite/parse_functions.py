from asyncio import StreamReader
from typing import AsyncGenerator, TypeVar

from bite.core import ParsedNode, Parser
from bite.io import ParserBuffer

T = TypeVar("T", covariant=True)
V = TypeVar("V", covariant=True)


async def parse_incremental(
    grammar: Parser[T, V], reader: StreamReader
) -> AsyncGenerator[ParsedNode[T, V], None]:
    buffer = ParserBuffer(reader)
    while not buffer.at_eof():
        parse_tree = await grammar.parse(buffer, 0)
        yield parse_tree
        await buffer.drop_prefix(parse_tree.end_loc)
