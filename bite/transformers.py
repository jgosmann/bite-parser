from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

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


class Suppress(Parser[ParsedNode[T, VIn], None]):
    def __init__(self, parser: Parser[T, VIn], *, name: str = None):
        super().__init__(name)
        self.parser = parser

    async def parse(
        self, buf: ParserBuffer, loc: int = 0
    ) -> ParsedTransform[Any, VIn, None]:
        return ParsedTransform(
            self.name, await self.parser.parse(buf, loc), lambda _: None
        )
