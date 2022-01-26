import pytest

from bite.io import ParserBuffer
from bite.parsers import (
    And,
    CaselessLiteral,
    CharacterSet,
    Literal,
    MatchFirst,
    ParsedAnd,
    ParsedCharacterSet,
    ParsedLiteral,
    ParsedMatchFirst,
    UnmetExpectationError,
)
from bite.tests.mock_reader import MockReader


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_buf,grammar,expected",
    [
        # Literals
        (
            b"LITERAL foo",
            Literal(b"LITERAL", name="literal"),
            ParsedLiteral("literal", b"LITERAL", 0, 7),
        ),
        (
            b"LiTeRaL foo",
            CaselessLiteral(b"lItErAl", name="literal"),
            ParsedLiteral("literal", b"lItErAl", 0, 7),
        ),
        # CharacterSet
        (
            b"123",
            CharacterSet(b"0123456789", name="charset"),
            ParsedCharacterSet("charset", b"1", 0, 1),
        ),
        (
            b"ABC",
            CharacterSet(b"0123456789", invert=True, name="inverted charset"),
            ParsedCharacterSet("inverted charset", b"A", 0, 1),
        ),
        # MatchFirst
        (
            b"A foo",
            MatchFirst([Literal(b"A"), Literal(b"B")]),
            ParsedMatchFirst(None, ParsedLiteral("b'A'", b"A", 0, 1), 0),
        ),
        (
            b"B foo",
            MatchFirst([Literal(b"A"), Literal(b"B")]),
            ParsedMatchFirst(None, ParsedLiteral("b'B'", b"B", 0, 1), 1),
        ),
        (
            b"A foo",
            MatchFirst(
                [Literal(b"A", name="first"), Literal(b"A", name="second")],
                name="precedence test",
            ),
            ParsedMatchFirst("precedence test", ParsedLiteral("first", b"A", 0, 1), 0),
        ),
        # And
        (
            b"AB foo",
            And([Literal(b"A"), Literal(b"B")], name="and"),
            ParsedAnd(
                "and",
                (ParsedLiteral("b'A'", b"A", 0, 1), ParsedLiteral("b'B'", b"B", 1, 2)),
            ),
        ),
    ],
)
async def test_successful_parsing(input_buf, grammar, expected):
    buffer = ParserBuffer(MockReader(input_buf))
    assert await grammar.parse(buffer) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_buf,grammar",
    [
        (b"foo", Literal(b"LITERAL")),
        (b"C", MatchFirst([Literal(b"A"), Literal(b"B")])),
        (b"A", CharacterSet(b"0123456789")),
        (b"0", CharacterSet(b"0123456789", invert=True)),
    ],
)
async def test_parsing_failure(input_buf, grammar):
    buffer = ParserBuffer(MockReader(input_buf))
    with pytest.raises(UnmetExpectationError) as excinfo:
        await grammar.parse(buffer)
    assert excinfo.value.expected == grammar
    assert excinfo.value.at_loc == 0


@pytest.mark.asyncio
async def test_parsing_failure_and():
    buffer = ParserBuffer(MockReader(b"AB"))

    grammar = And([Literal(b"C"), Literal(b"B")])
    with pytest.raises(UnmetExpectationError) as excinfo:
        await grammar.parse(buffer)
    assert excinfo.value.expected == grammar.parsers[0]
    assert excinfo.value.at_loc == 0

    grammar = And([Literal(b"A"), Literal(b"C")])
    with pytest.raises(UnmetExpectationError) as excinfo:
        await grammar.parse(buffer)
    assert excinfo.value.expected == grammar.parsers[1]
    assert excinfo.value.at_loc == 1


def test_parsed_match_first_loc_range():
    parsed_one_of = ParsedMatchFirst(None, ParsedLiteral(None, b"val", 4, 7), 0)
    assert parsed_one_of.start_loc == 4
    assert parsed_one_of.end_loc == 7


def test_parsed_and_loc_range():
    parsed_and = ParsedAnd(
        None, (ParsedLiteral(None, b"val", 4, 7), ParsedLiteral(None, b"val", 7, 10))
    )
    assert parsed_and.start_loc == 4
    assert parsed_and.end_loc == 10
