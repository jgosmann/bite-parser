from dataclasses import dataclass
from typing import Generic, Iterable, Optional, Protocol, TypeVar

from bite.io import ParserBuffer

T = TypeVar("T")


class ParsedNode(Protocol[T]):
    name: Optional[str]
    value: T

    @property
    def start_loc(self) -> int:
        ...

    @property
    def end_loc(self) -> int:
        ...


@dataclass
class ParsedBaseNode(Generic[T]):
    name: Optional[str]
    value: T


@dataclass
class ParsedLeaf(ParsedBaseNode[T]):
    name: Optional[str]
    value: T
    start_loc: int
    end_loc: int


class Parser(Generic[T]):
    def __init__(self, name=None):
        self.name = name

    def __str__(self) -> str:
        return self.name if self.name else super().__str__()

    async def parse(self, buf: ParserBuffer, loc: int = 0) -> ParsedNode[T]:
        raise NotImplementedError()


ParsedLiteral = ParsedLeaf[bytes]


class Literal(Parser[bytes]):
    def __init__(self, literal: bytes, *, name: str = None):
        super().__init__(name if name else str(literal))
        self.literal = literal

    async def parse(self, buf: ParserBuffer, loc: int = 0) -> ParsedLiteral:
        end_loc = loc + len(self.literal)
        peek = await buf.get(slice(loc, end_loc))
        if peek == self.literal:
            return ParsedLiteral(self.name, self.literal, loc, end_loc)
        else:
            raise UnmetExpectationError(self, loc)


class CaselessLiteral(Parser[bytes]):
    def __init__(self, literal: bytes, *, name: str = None):
        super().__init__(name if name else str(literal))
        self.literal = literal
        self._lowercased_literal = self.literal.lower()

    async def parse(self, buf: ParserBuffer, loc: int = 0) -> ParsedLiteral:
        end_loc = loc + len(self.literal)
        peek = await buf.get(slice(loc, end_loc))
        if peek.lower() == self._lowercased_literal:
            return ParsedLiteral(self.name, self.literal, loc, end_loc)
        else:
            raise UnmetExpectationError(self, loc)


ParsedCharacterSet = ParsedLeaf[bytes]


class CharacterSet(Parser[bytes]):
    def __init__(
        self, charset: Iterable[int], *, invert: bool = False, name: str = None
    ):
        super().__init__(name if name else f"CharacterSet({charset})")
        self.charset = frozenset(charset)
        self.invert = invert

    async def parse(self, buf: ParserBuffer, loc: int = 0) -> ParsedCharacterSet:
        char = await buf.get(loc)
        if len(char) == 1 and (char[0] in self.charset) != self.invert:
            return ParsedCharacterSet(self.name, char, loc, loc + 1)
        else:
            raise UnmetExpectationError(self, loc)


@dataclass
class ParsedOneOf(ParsedBaseNode[ParsedNode]):
    choice_index: int

    @property
    def start_loc(self) -> int:
        return self.value.start_loc

    @property
    def end_loc(self) -> int:
        return self.value.end_loc


class OneOf(Parser[ParsedNode]):
    def __init__(self, choices: Iterable[Parser], *, name: str = None):
        super().__init__(name)
        self.choices = choices

    def __str__(self):
        return " | ".join(f"({choice})" for choice in self.choices)

    async def parse(self, buf: ParserBuffer, loc: int = 0) -> ParsedOneOf:
        for i, choice in enumerate(self.choices):
            try:
                parsed_node = await choice.parse(buf, loc)
                return ParsedOneOf(self.name, parsed_node, i)
            except UnmetExpectationError:
                pass
        raise UnmetExpectationError(self, loc)


class ParseError(Exception):
    pass


class UnmetExpectationError(ParseError):
    def __init__(self, expected: Parser, at_loc: int):
        super().__init__(f"expected {expected} at position {at_loc}")
        self.expected = expected
        self.at_loc = at_loc
