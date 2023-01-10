from dataclasses import dataclass
from typing import Callable, Generic, Iterable, Optional, Tuple, TypeVar

from bite.io import ParserBuffer
from bite.parsers import ParsedBaseNode, ParsedNode, Parser

T = TypeVar("T", covariant=True)
VIn_co = TypeVar("VIn_co", covariant=True)
VOut_co = TypeVar("VOut_co", covariant=True)


@dataclass(frozen=True)
class ParsedTransform(
    ParsedBaseNode[ParsedNode[T, VIn_co]], Generic[T, VIn_co, VOut_co]
):
    transform: Callable[[ParsedNode[T, VIn_co]], Iterable[VOut_co]]
    """Function to transfrom the child nodes."""

    @property
    def values(self) -> Iterable[VOut_co]:
        """Transformed values of the child nodes."""
        # for some reason mypy thinks transform is a bare object
        return self.transform(self.parse_tree)  # type: ignore

    @property
    def start_loc(self) -> int:
        """Start index into the input buffer of the segmend parsed by the
        node."""
        return self.parse_tree.start_loc

    @property
    def end_loc(self) -> int:
        """End index (exclusive) into the input buffer of the segmend parsed by
        the node."""
        return self.parse_tree.end_loc


class Transform(Parser[ParsedNode[T, VIn_co], VOut_co]):
    """Transform a resulting parse tree node to produce different values.

    Parameters
    ----------
    parser:
        Parser of which the resulting parse tree will be transformed.
    transform:
        Function that takes the parse tree produced by the *parser* and produces
        the transformed values.
    name:
        Name to assign to the resulting parse tree node.

    See Also
    --------
    .TransformValues: Passes only the parse tree node values instead of the
        complete node to the *transform*.

    Examples
    --------

    .. testcode:: transform

        import asyncio
        from bite import CharacterSet, Combine, parse_bytes, Transform

        integer_token = Combine(CharacterSet(b'0123456789')[1, ...])
        print(asyncio.run(parse_bytes(integer_token, b'42')).values)
        print(asyncio.run(parse_bytes(
            Transform(integer_token, lambda node: (int(node.parse_tree),)),
            b'42'
        )).values)

    .. testoutput:: transform

        (b'42',)
        (42,)
    """

    def __init__(
        self,
        parser: Parser[T, VIn_co],
        transform: Callable[[ParsedNode[T, VIn_co]], Iterable[VOut_co]],
        *,
        name: Optional[str] = None,
    ):
        super().__init__(name if name else f"Transform({parser.name})")
        self.parser = parser
        self.transform = transform

    async def parse(
        self, buf: ParserBuffer, loc: int = 0
    ) -> ParsedTransform[T, VIn_co, VOut_co]:
        return ParsedTransform(
            self.name, await self.parser.parse(buf, loc), self.transform
        )


class Suppress(Transform[T, VIn_co, None]):
    """Suppresses a parse tree from the values.

    Parameters
    ----------
    parser:
        Parser of which the resulting parse tree will be suppressed.
    name:
        Name to assign to the resulting parse tree node.

    Examples
    --------

    .. testcode:: suppress

        import asyncio
        from bite import CharacterSet, Combine, Literal, parse_bytes, Suppress

        integer_token = Combine(CharacterSet(b'0123456789')[1, ...])
        print(asyncio.run(parse_bytes(
            Suppress(Literal(b'[')) + integer_token + Suppress(Literal(b']')),
            b'[42]'
        )).values)

    .. testoutput:: suppress

        (b'42',)
    """

    def __init__(self, parser: Parser[T, VIn_co], *, name: Optional[str] = None):
        super().__init__(
            parser, lambda _: [], name=name if name else f"Suppress({parser.name})"
        )


class TransformValues(Transform[T, VIn_co, VOut_co]):
    """Transform parsed values.

    Parameters
    ----------
    parser:
        Parser of which the resulting parse tree values will be transformed.
    transform:
        Function that takes the values produced by the *parser* and produces
        the transformed values.
    name:
        Name to assign to the resulting parse tree node.

    See Also
    --------
    .Transform: Passes the complete parse tree node instead of just the values
        to the *transform*.

    Examples
    --------

    .. testcode:: transform-values

        import asyncio
        from bite import CharacterSet, Combine, Literal, parse_bytes, TransformValues

        def sum_values(values):
            return (sum(int(v) for v in values if v != b'+'),)

        integer_token = Combine(CharacterSet(b'0123456789')[1, ...])
        print(asyncio.run(parse_bytes(
            TransformValues(integer_token + Literal(b'+') + integer_token, sum_values),
            b'42+23'
        )).values)

    .. testoutput:: transform-values

        (65,)
    """

    def __init__(
        self,
        parser: Parser[T, VIn_co],
        transform: Callable[[Iterable[VIn_co]], Iterable[VOut_co]],
        *,
        name: Optional[str] = None,
    ):
        super().__init__(
            parser,
            lambda parse_tree: transform(parse_tree.values),
            name=name if name else f"TransformValues({parser.name})",
        )


class Group(TransformValues[T, VIn_co, Tuple[VIn_co, ...]]):
    """Group the values of a resulting parse tree node into a tuple.

    This allows to introduce structure into the otherwise flat
    :attr:`ParsedNote.value` tuple.

    Parameters
    ----------
    parser:
        Parser of which the resulting parse tree values will be grouped.
    name:
        Name to assign to the resulting parse tree node.

    Examples
    --------

    .. testcode:: group

        import asyncio
        from bite import CharacterSet, Combine, Group, Literal, parse_bytes, Suppress

        item = Combine(CharacterSet(b'[],', invert=True))
        delimited_list = Group(
            Suppress(Literal(b'['))
            + item
            + (Suppress(Literal(b',')) + item)[0, ...]
            + Suppress(Literal(b']'))
        )
        print(asyncio.run(parse_bytes(
            delimited_list[0, ...],
            b'[A,B][1,2,3]'
        )).values)

    .. testoutput:: group

        ((b'A', b'B'), (b'1', b'2', b'3'))
    """

    def __init__(self, parser: Parser[T, VIn_co], *, name: Optional[str] = None):
        super().__init__(
            parser,
            lambda values: (tuple(values),),
            name=name if name else f"Group({parser.name})",
        )


__all__ = [
    "Group",
    "Suppress",
    "Transform",
    "TransformValues",
]
