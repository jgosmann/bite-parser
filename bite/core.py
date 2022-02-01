import itertools
from dataclasses import dataclass
from typing import Any, Generic, Iterable, NoReturn, Optional, Tuple, TypeVar, Union

from typing_extensions import Protocol

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
    def values(self) -> Iterable[V]:
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
    def values(self) -> Tuple[T]:
        return (self.parse_tree,)


@dataclass(frozen=True)
class ParsedNil:
    name: Optional[str]
    loc: int

    @property
    def parse_tree(self) -> None:
        return None

    @property
    def values(self) -> Tuple[()]:
        return ()

    @property
    def start_loc(self) -> int:
        return self.loc

    @property
    def end_loc(self) -> int:
        return self.loc


class Parser(Generic[T, V]):
    def __init__(self, name=None):
        self.name = name

    def __str__(self) -> str:
        return self.name if self.name else super().__str__()

    async def parse(self, buf: ParserBuffer, loc: int = 0) -> ParsedNode[T, V]:
        raise NotImplementedError()

    def __add__(self, other: "Parser") -> "And":
        return And((self, other), name=f"({self}) + ({other})")

    def __or__(self, other: "Parser") -> "MatchFirst":
        return MatchFirst((self, other), name=f"({self}) | ({other})")

    def __invert__(self) -> "Not":
        return Not(self)

    def __getitem__(
        self, repeats: Union[int, Tuple[int, Union[int, "ellipsis", None]]]
    ) -> "Repeat":
        if isinstance(repeats, int):
            min_repeats = repeats
            max_repeats: Optional[int] = repeats
        else:
            min_repeats = repeats[0]
            max_repeats = repeats[1] if isinstance(repeats[1], int) else None
        return Repeat(
            self,
            min_repeats,
            max_repeats,
            name=f"({self})[{min_repeats}, {'...' if max_repeats is None else max_repeats}]",
        )


@dataclass(frozen=True)
class ParsedMatchFirst(ParsedBaseNode[ParsedNode[T, V]]):
    choice_index: int

    @property
    def values(self) -> Iterable[V]:
        return self.parse_tree.values

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

    def __or__(self, other: "Parser") -> "MatchFirst":
        return MatchFirst(tuple(self.choices) + (other,), name=f"{self} | ({other})")


@dataclass(frozen=True)
class ParsedList(ParsedBaseNode[Tuple[ParsedNode[T, V], ...]]):
    loc: int

    @property
    def values(self) -> Tuple[V, ...]:
        return tuple(
            itertools.chain.from_iterable(node.values for node in self.parse_tree)
        )

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


class And(Parser[Tuple[ParsedNode, ...], Any]):
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

    def __add__(self, other: "Parser") -> "And":
        return And(tuple(self.parsers) + (other,), name=f"{self} + ({other})")


ParsedRepeat = ParsedList


class Repeat(Parser[Tuple[ParsedNode[T, V], ...], V]):
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


class Not(Parser[None, NoReturn]):
    def __init__(self, parser: Parser[Any, Any], *, name: str = None):
        super().__init__(name if name else f"Not({parser})")
        self.parser = parser

    async def parse(self, buf: ParserBuffer, loc: int = 0) -> ParsedNil:
        try:
            await self.parser.parse(buf, loc)
        except UnmetExpectationError:
            return ParsedNil(self.name, loc)
        else:
            raise UnmetExpectationError(self, loc)


class Forward(Parser[T, V]):
    def __init__(self, parser: Parser[T, V] = None, *, name: str = None):
        super().__init__(name if name else "forward")
        self.parser = parser

    def assign(self, parser: Parser[T, V]):
        self.parser = parser

    async def parse(self, buf: ParserBuffer, loc: int = 0) -> ParsedNode[T, V]:
        if self.parser is None:
            raise ValueError("unassigned forward parser")
        return await self.parser.parse(buf, loc)


class ParseError(Exception):
    pass


class UnmetExpectationError(ParseError):
    def __init__(self, expected: Parser, at_loc: int):
        super().__init__(f"expected {expected} at position {at_loc}")
        self.expected = expected
        self.at_loc = at_loc


class TrailingBytesError(ParseError):
    pass


__all__ = [
    "And",
    "Forward",
    "MatchFirst",
    "Not",
    "Parser",
    "ParseError",
    "ParsedNode",
    "Repeat",
    "TrailingBytesError",
    "UnmetExpectationError",
]
