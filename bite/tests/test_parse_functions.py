import pytest

from bite.parse_functions import parse_incremental
from bite.parsers import Literal, ParsedLiteral
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
