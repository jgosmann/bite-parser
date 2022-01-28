import pytest

from bite.io import ParserBuffer
from bite.parsers import (
    And,
    CaselessLiteral,
    CharacterSet,
    Counted,
    FixedByteCount,
    Literal,
    MatchFirst,
    ParsedAnd,
    ParsedCharacterSet,
    ParsedFixedByteCount,
    ParsedLeaf,
    ParsedLiteral,
    ParsedMatchFirst,
    UnmetExpectationError,
)
from bite.tests.mock_reader import MockReader
from bite.transformers import ParsedTransform, Suppress, TransformValue


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_buf,grammar,expected",
    [
        # Literals
        (
            b"LITERAL foo",
            Literal(b"LITERAL", name="literal"),
            ParsedLiteral("literal", b"LITERAL", 4, 11),
        ),
        (
            b"LiTeRaL foo",
            CaselessLiteral(b"lItErAl", name="literal"),
            ParsedLiteral("literal", b"lItErAl", 4, 11),
        ),
        # CharacterSet
        (
            b"123",
            CharacterSet(b"0123456789", name="charset"),
            ParsedCharacterSet("charset", b"1", 4, 5),
        ),
        (
            b"ABC",
            CharacterSet(b"0123456789", invert=True, name="inverted charset"),
            ParsedCharacterSet("inverted charset", b"A", 4, 5),
        ),
        # FixedByteCount
        (
            b"0123456789",
            FixedByteCount(4, name="fixed length"),
            ParsedFixedByteCount("fixed length", b"0123", 4, 8),
        ),
        # MatchFirst
        (
            b"A foo",
            MatchFirst([Literal(b"A"), Literal(b"B")]),
            ParsedMatchFirst(None, ParsedLiteral("b'A'", b"A", 4, 5), 0),
        ),
        (
            b"B foo",
            MatchFirst([Literal(b"A"), Literal(b"B")]),
            ParsedMatchFirst(None, ParsedLiteral("b'B'", b"B", 4, 5), 1),
        ),
        (
            b"A foo",
            MatchFirst(
                [Literal(b"A", name="first"), Literal(b"A", name="second")],
                name="precedence test",
            ),
            ParsedMatchFirst("precedence test", ParsedLiteral("first", b"A", 4, 5), 0),
        ),
        # And
        (
            b"AB foo",
            And([Literal(b"A"), Literal(b"B")], name="and"),
            ParsedAnd(
                "and",
                (ParsedLiteral("b'A'", b"A", 4, 5), ParsedLiteral("b'B'", b"B", 5, 6)),
            ),
        ),
    ],
)
async def test_successful_parsing(input_buf, grammar, expected):
    buffer = ParserBuffer(MockReader(b"foo " + input_buf))
    assert await grammar.parse(buffer, 4) == expected


@pytest.mark.asyncio
async def test_successful_counted_parsing():
    buffer = ParserBuffer(MockReader(b"foo [4]0123456789"))
    grammar = Counted(
        TransformValue(
            And(
                [
                    Suppress(Literal(b"[")),
                    CharacterSet(b"0123456789"),
                    Suppress(Literal(b"]")),
                ]
            ),
            lambda value: int(value[0]),
            name="transform",
        ),
        lambda count: FixedByteCount(count, name="fixed byte count"),
    )
    parsed = await grammar.parse(buffer, 4)

    assert parsed.parse_tree.count_expr.name == "transform"
    assert parsed.parse_tree.count_expr.value == 4
    assert parsed.parse_tree.counted_expr == ParsedFixedByteCount(
        "fixed byte count", b"0123", 7, 11
    )
    assert parsed.value == b"0123"


@pytest.mark.asyncio
@pytest.mark.parametrize("input_buf, at_loc", [(b"[4x012345689]", 2), (b"[4]01", 3)])
async def test_unsuccessful_counted_parsing(input_buf, at_loc):
    buffer = ParserBuffer(MockReader(input_buf))
    grammar = Counted(
        TransformValue(
            And(
                [
                    Suppress(Literal(b"[")),
                    CharacterSet(b"0123456789"),
                    Suppress(Literal(b"]")),
                ]
            ),
            lambda value: int(value[0]),
            name="transform",
        ),
        lambda count: FixedByteCount(count, name="fixed byte count"),
    )

    with pytest.raises(UnmetExpectationError) as excinfo:
        await grammar.parse(buffer)
    assert excinfo.value.at_loc == at_loc


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_buf,grammar",
    [
        (b"foo", Literal(b"LITERAL")),
        (b"C", MatchFirst([Literal(b"A"), Literal(b"B")])),
        (b"A", CharacterSet(b"0123456789")),
        (b"0", CharacterSet(b"0123456789", invert=True)),
        (b"0123", FixedByteCount(6)),
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


@pytest.mark.parametrize(
    "parse_tree,expected_value",
    [
        (ParsedLeaf("leaf", b"foo", 0, 3), b"foo"),
        (ParsedMatchFirst("match-first", ParsedLeaf("leaf", b"foo", 0, 3), 0), b"foo"),
        (
            ParsedAnd(
                "and",
                (
                    ParsedTransform(
                        "suppress", ParsedLeaf("x", b"x", 0, 1), lambda _: None
                    ),
                    ParsedLeaf("leaf", b"foo", 1, 4),
                ),
            ),
            [b"foo"],
        ),
    ],
)
def test_parsed_vaule(parse_tree, expected_value):
    assert parse_tree.value == expected_value


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
