from dataclasses import dataclass
from typing import Generic, Optional, Protocol, TypeVar

from bite.io import ParserBuffer

T = TypeVar("T", covariant=True)
V = TypeVar("V", covariant=True)


class ParsedNode(Protocol[T, V]):
    @property
    def name(self) -> Optional[str]:
        ...

    @property
    def parse_tree(self) -> T:
        ...

    @property
    def value(self) -> V:
        ...

    @property
    def start_loc(self) -> int:
        ...

    @property
    def end_loc(self) -> int:
        ...


@dataclass(frozen=True)
class ParsedBaseNode(Generic[T]):
    name: Optional[str]
    parse_tree: T


@dataclass(frozen=True)
class ParsedLeaf(ParsedBaseNode[T]):
    name: Optional[str]
    parse_tree: T
    start_loc: int
    end_loc: int

    @property
    def value(self) -> T:
        return self.parse_tree


class Parser(Generic[T, V]):
    def __init__(self, name=None):
        self.name = name

    def __str__(self) -> str:
        return self.name if self.name else super().__str__()

    async def parse(self, buf: ParserBuffer, loc: int = 0) -> ParsedNode[T, V]:
        raise NotImplementedError()


class ParseError(Exception):
    pass


class UnmetExpectationError(ParseError):
    def __init__(self, expected: Parser, at_loc: int):
        super().__init__(f"expected {expected} at position {at_loc}")
        self.expected = expected
        self.at_loc = at_loc
