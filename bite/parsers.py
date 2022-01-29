import itertools
from dataclasses import dataclass
from typing import Any, Callable, Generic, Iterable, List, Optional, Tuple, TypeVar

from bite.core import (
    ParsedBaseNode,
    ParsedLeaf,
    ParsedNode,
    Parser,
    UnmetExpectationError,
)
from bite.io import ParserBuffer

T = TypeVar("T", covariant=True)
V = TypeVar("V", covariant=True)

ParsedLiteral = ParsedLeaf[bytes]


class Literal(Parser[bytes, bytes]):
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


class CaselessLiteral(Parser[bytes, bytes]):
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


class CharacterSet(Parser[bytes, bytes]):
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


ParsedFixedByteCount = ParsedLeaf[bytes]


class FixedByteCount(Parser[bytes, bytes]):
    def __init__(self, count: int, *, name: str = None):
        super().__init__(name if name else f"FixedByteCount({count})")
        self.count = count

    async def parse(self, buf: ParserBuffer, loc: int = 0) -> ParsedFixedByteCount:
        read_bytes = await buf.get(slice(loc, loc + self.count))
        if len(read_bytes) == self.count:
            return ParsedFixedByteCount(
                self.name, read_bytes, loc, loc + len(read_bytes)
            )
        else:
            raise UnmetExpectationError(self, loc)


@dataclass(frozen=True)
class ParsedMatchFirst(ParsedBaseNode[ParsedNode[T, T]]):
    choice_index: int

    @property
    def value(self) -> T:
        return self.parse_tree.value

    @property
    def start_loc(self) -> int:
        return self.parse_tree.start_loc

    @property
    def end_loc(self) -> int:
        return self.parse_tree.end_loc


class MatchFirst(Parser[ParsedNode[Any, V], V]):
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
class ParsedList(ParsedBaseNode[Tuple[ParsedNode[T, V], ...]]):
    loc: int

    @property
    def value(self) -> List[V]:
        values = (node.value for node in self.parse_tree)
        return [value for value in values if value is not None]

    @property
    def start_loc(self) -> int:
        if len(self.parse_tree) > 0:
            return self.parse_tree[0].start_loc
        else:
            return self.loc

    @property
    def end_loc(self) -> int:
        if len(self.parse_tree) > 0:
            return self.parse_tree[-1].end_loc
        else:
            return self.loc


ParsedAnd = ParsedList[Any, Any]


class And(Parser[Tuple[ParsedNode, ...], List]):
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
        return ParsedAnd(self.name, tuple(parsed_nodes), loc)


ParsedRepeat = ParsedList


class Repeat(Parser[Tuple[ParsedNode[T, V], ...], List[V]]):
    def __init__(
        self,
        parser: Parser[T, V],
        min_repeats: int = 0,
        max_repeats: int = None,
        *,
        name: str = None,
    ):
        super().__init__(name)
        self.parser = parser
        self.min_repeats = min_repeats
        self.max_repeats = max_repeats

    def __str__(self):
        return f"({self.parser})[{self.min_repeats}, {self.max_repeats}]"

    async def parse(self, buf: ParserBuffer, loc: int = 0) -> ParsedRepeat:
        current_loc = loc
        parsed = []
        for _ in range(self.min_repeats):
            parsed.append(await self.parser.parse(buf, current_loc))
            current_loc = parsed[-1].end_loc

        for i in itertools.count(self.min_repeats):
            if self.max_repeats is not None and i >= self.max_repeats:
                break
            try:
                parsed.append(await self.parser.parse(buf, current_loc))
                current_loc = parsed[-1].end_loc
            except UnmetExpectationError:
                break

        return ParsedRepeat(self.name, tuple(parsed), loc)


ParsedZeroOrMore = ParsedRepeat


class ZeroOrMore(Repeat[T, V]):
    def __init__(self, parser: Parser[T, V], *, name: str = None):
        super().__init__(parser, min_repeats=0, name=name)


ParsedOneOrMore = ParsedRepeat


class OneOrMore(Repeat[T, V]):
    def __init__(self, parser: Parser[T, V], *, name: str = None):
        super().__init__(parser, min_repeats=1, name=name)


@dataclass(frozen=True)
class ParsedOpt(ParsedBaseNode[Optional[ParsedNode[T, V]]]):
    loc: int

    @property
    def value(self) -> Optional[V]:
        if self.parse_tree:
            return self.parse_tree.value
        else:
            return None

    @property
    def start_loc(self) -> int:
        if self.parse_tree:
            return self.parse_tree.start_loc
        else:
            return self.loc

    @property
    def end_loc(self) -> int:
        if self.parse_tree:
            return self.parse_tree.end_loc
        else:
            return self.loc


class Opt(Parser[Optional[ParsedNode[T, V]], Optional[V]]):
    def __init__(self, parser: Parser[T, V], *, name: str = None):
        super().__init__(name if name else f"Opt({parser})")
        self.parser = parser

    async def parse(self, buf: ParserBuffer, loc: int = 0):
        try:
            return ParsedOpt(self.name, await self.parser.parse(buf, loc), loc)
        except UnmetExpectationError:
            # Somehow mypy doesn't recognize the parse tree as optional
            return ParsedOpt(self.name, None, loc)  # type: ignore


@dataclass(frozen=True)
class CountedParseTree:
    count_expr: ParsedNode[Any, int]
    counted_expr: ParsedNode

    @property
    def start_loc(self) -> int:
        return self.count_expr.start_loc

    @property
    def end_loc(self) -> int:
        return self.counted_expr.end_loc


@dataclass(frozen=True)
class ParsedCounted(ParsedBaseNode[CountedParseTree], Generic[V]):
    @property
    def value(self) -> V:
        return self.parse_tree.counted_expr.value

    @property
    def start_loc(self) -> int:
        return self.parse_tree.start_loc

    @property
    def end_loc(self) -> int:
        return self.parse_tree.end_loc


class Counted(Parser[CountedParseTree, V]):
    def __init__(
        self,
        count_parser: Parser[Any, int],
        counted_parser_factory: Callable[[int], Parser[Any, V]],
        *,
        name: str = None,
    ):
        super().__init__(
            name if name else f"Counted({count_parser.name}, {counted_parser_factory})"
        )
        self.count_parser = count_parser
        self.counted_parser_factory = counted_parser_factory

    async def parse(self, buf: ParserBuffer, loc: int = 0) -> ParsedCounted[V]:
        count = await self.count_parser.parse(buf, loc)
        counted = await self.counted_parser_factory(count.value).parse(
            buf, count.end_loc
        )
        return ParsedCounted(self.name, CountedParseTree(count, counted))
