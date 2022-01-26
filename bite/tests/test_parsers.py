import pytest

from bite.io import ParserBuffer
from bite.parsers import (
    Literal,
    OneOf,
    ParsedLiteral,
    ParsedOneOf,
    UnmetExpectationError,
)
from bite.tests.mock_reader import MockReader


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_buf,grammar,expected",
    [
        # Literals
        (
            b"LITERAL",
            Literal(b"LITERAL", "literal"),
            ParsedLiteral("literal", b"LITERAL", 0, 7),
        ),
        # OneOf
        (
            b"A",
            OneOf([Literal(b"A"), Literal(b"B")]),
            ParsedOneOf(None, ParsedLiteral("b'A'", b"A", 0, 1), 0),
        ),
        (
            b"B",
            OneOf([Literal(b"A"), Literal(b"B")]),
            ParsedOneOf(None, ParsedLiteral("b'B'", b"B", 0, 1), 1),
        ),
        (
            b"A",
            OneOf(
                [Literal(b"A", name="first"), Literal(b"A", name="second")],
                name="precedence test",
            ),
            ParsedOneOf("precedence test", ParsedLiteral("first", b"A", 0, 1), 0),
        ),
    ],
)
async def test_successful_parsing(input_buf, grammar, expected):
    buffer = ParserBuffer(MockReader(input_buf))
    assert await grammar.parse(buffer) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_buf,grammar",
    [(b"foo", Literal(b"LITERAL")), (b"C", OneOf([Literal(b"A"), Literal(b"B")]))],
)
async def test_parsing_failure(input_buf, grammar):
    buffer = ParserBuffer(MockReader(input_buf))
    with pytest.raises(UnmetExpectationError) as excinfo:
        await grammar.parse(buffer)
    assert excinfo.value.expected == grammar
    assert excinfo.value.at_loc == 0


def test_parsed_one_of_loc_range():
    parsed_one_of = ParsedOneOf(None, ParsedLiteral(None, b"val", 4, 7), 0)
    assert parsed_one_of.start_loc == 4
    assert parsed_one_of.end_loc == 7
