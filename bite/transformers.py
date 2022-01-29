from dataclasses import dataclass
from typing import Callable, Generic, Iterable, TypeVar

from bite.core import ParsedBaseNode, ParsedNode, Parser
from bite.io import ParserBuffer

T = TypeVar("T", covariant=True)
VIn = TypeVar("VIn", covariant=True)
VOut = TypeVar("VOut", covariant=True)


@dataclass(frozen=True)
class ParsedTransform(ParsedBaseNode[ParsedNode[T, VIn]], Generic[T, VIn, VOut]):
    transform: Callable[[ParsedNode[T, VIn]], VOut]

    @property
    def value(self) -> VOut:
        # for some reason my thinks transform is a bare object
        return self.transform(self.parse_tree)  # type: ignore

    @property
    def start_loc(self) -> int:
        return self.parse_tree.start_loc

    @property
    def end_loc(self) -> int:
        return self.parse_tree.end_loc


class Transform(Parser[ParsedNode[T, VIn], VOut]):
    def __init__(
        self,
        parser: Parser[T, VIn],
        transform: Callable[[ParsedNode[T, VIn]], VOut],
        *,
        name: str = None,
    ):
        super().__init__(name if name else f"Transform({parser.name})")
        self.parser = parser
        self.transform = transform

    async def parse(
        self, buf: ParserBuffer, loc: int = 0
    ) -> ParsedTransform[T, VIn, VOut]:
        return ParsedTransform(
            self.name, await self.parser.parse(buf, loc), self.transform
        )


class Suppress(Transform[T, VIn, None]):
    def __init__(self, parser: Parser[T, VIn], *, name: str = None):
        super().__init__(
            parser, lambda _: None, name=name if name else f"Suppress({parser.name})"
        )


class TransformValue(Transform[T, VIn, VOut]):
    def __init__(
        self,
        parser: Parser[T, VIn],
        transform: Callable[[VIn], VOut],
        *,
        name: str = None,
    ):
        super().__init__(
            parser,
            lambda parse_tree: transform(parse_tree.value),
            name=name if name else f"TransformValue({parser.name})",
        )


class OnlyValue(TransformValue[T, Iterable[VIn], VIn]):
    def __init__(self, parser: Parser[T, Iterable[VIn]], *, name: str = None):
        super().__init__(
            parser,
            self._extract_only_value,
            name=name if name else f"OnlyValue({parser.name})",
        )

    @classmethod
    def _extract_only_value(cls, values: Iterable[VIn]) -> VIn:
        value_iter = iter(values)
        try:
            value = next(value_iter)
        except StopIteration:
            raise ValueError("expected exactly one value, found no values") from None
        try:
            next(value_iter)
            raise ValueError("expected exactly one value, found multiple values")
        except StopIteration:
            return value
