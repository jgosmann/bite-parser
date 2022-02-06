import pytest

from bite.parse_functions import parse_bytes, parse_incremental
from bite.parsers import Literal, ParsedLiteral, TrailingBytesError
from bite.tests.mock_reader import MockReader


@pytest.mark.asyncio
async def test_parse_incremental():
    grammar = Literal(b"A", name="A")
    reader = MockReader(b"AAA")

    count = 0
    async for parse_tree in parse_incremental(grammar, reader):
        assert parse_tree == ParsedLiteral("A", b"A", 0, 1)
        count += 1

    assert count == 3


@pytest.mark.asyncio
async def test_parse_bytes():
    grammar = Literal(b"A", name="A")
    assert await parse_bytes(grammar, b"AAA") == ParsedLiteral("A", b"A", 0, 1)


@pytest.mark.asyncio
async def test_parse_bytes_parse_all():
    grammar = Literal(b"A", name="A")
    assert await parse_bytes(grammar, b"A", parse_all=True) == ParsedLiteral(
        "A", b"A", 0, 1
    )


@pytest.mark.asyncio
async def test_parse_bytes_parse_all_failure():
    grammar = Literal(b"A", name="A")
    with pytest.raises(TrailingBytesError):
        assert await parse_bytes(grammar, b"AA", parse_all=True)
