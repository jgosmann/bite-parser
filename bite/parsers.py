from dataclasses import dataclass
from typing import Generic, Iterable, Optional, Protocol, Tuple, TypeVar

from bite.io import ParserBuffer

T = TypeVar("T", covariant=True)


class ParsedNode(Protocol[T]):
    @property
    def name(self) -> Optional[str]:
        ...

    @property
    def parse_tree(self) -> T:
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


@dataclass(frozen=True)
class ParsedMatchFirst(ParsedBaseNode[ParsedNode]):
    choice_index: int

    @property
    def start_loc(self) -> int:
        return self.parse_tree.start_loc

    @property
    def end_loc(self) -> int:
        return self.parse_tree.end_loc


class MatchFirst(Parser[ParsedNode]):
    def __init__(self, choices: Iterable[Parser], *, name: str = None):
        super().__init__(name)
        self.choices = choices

    def __str__(self):
        return " | ".join(f"({choice})" for choice in self.choices)

    async def parse(self, buf: ParserBuffer, loc: int = 0) -> ParsedMatchFirst:
        for i, choice in enumerate(self.choices):
            try:
                parsed_node = await choice.parse(buf, loc)
                return ParsedMatchFirst(self.name, parsed_node, i)
            except UnmetExpectationError:
                pass
        raise UnmetExpectationError(self, loc)


@dataclass(frozen=True)
class ParsedAnd(ParsedBaseNode[Tuple[ParsedNode, ...]]):
    @property
    def start_loc(self) -> int:
        return self.parse_tree[0].start_loc

    @property
    def end_loc(self) -> int:
        return self.parse_tree[-1].end_loc


class And(Parser[Tuple[ParsedNode, ...]]):
    def __init__(self, parsers: Iterable[Parser], *, name: str = None):
        super().__init__(name)
        self.parsers = parsers

    def __str__(self):
        return " + ".join(f"({parser})" for parser in self.parsers)

    async def parse(self, buf: ParserBuffer, loc: int = 0) -> ParsedAnd:
        current_loc = loc
        parsed_nodes = []
        for parser in self.parsers:
            parsed_nodes.append(await parser.parse(buf, current_loc))
            current_loc = parsed_nodes[-1].end_loc
        return ParsedAnd(self.name, tuple(parsed_nodes))


class ParseError(Exception):
    pass


class UnmetExpectationError(ParseError):
    def __init__(self, expected: Parser, at_loc: int):
        super().__init__(f"expected {expected} at position {at_loc}")
        self.expected = expected
        self.at_loc = at_loc
