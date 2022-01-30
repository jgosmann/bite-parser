import pytest

from bite.io import BytesBuffer
from bite.parsers import Literal, ParsedLiteral
from bite.transformers import (
    Group,
    ParsedTransform,
    Suppress,
    Transform,
    TransformValues,
)


def test_parsed_transform():
    subtree = ParsedLiteral("literal", b"LITERAL", 0, 7)

    def transform(arg):
        assert arg == subtree
        return ["transformed value"]

    parsed_transform = ParsedTransform("name", subtree, transform)
    assert parsed_transform.name == "name"
    assert parsed_transform.values == ["transformed value"]
    assert parsed_transform.start_loc == 0
    assert parsed_transform.end_loc == 7


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_buf,grammar,expected_values",
    [
        # Group
        (
            b"ABBA",
            Literal(b"A", name="A")
            + Group(Literal(b"B", name="B")[1, ...])
            + Literal(b"A", name="A"),
            (b"A", (b"B", b"B"), b"A"),
        ),
        # Suppress
        (
            b"LITERAL",
            Suppress(Literal(b"LITERAL", name="literal")),
            [],
        ),
        # Transform
        (
            b"42",
            Transform(
                Literal(b"42"), lambda parse_tree: [int(v) for v in parse_tree.values]
            ),
            [42],
        ),
        # TransformValue
        (
            b"42",
            TransformValues(Literal(b"42"), lambda values: [int(v) for v in values]),
            [42],
        ),
    ],
)
async def test_successful_parsing(input_buf, grammar, expected_values):
    buffer = BytesBuffer(input_buf)
    parse_tree = await grammar.parse(buffer)
    assert parse_tree.values == expected_values
