from asyncio import StreamReader
from typing import Union

from typing_extensions import Protocol


def _copy_doc(source):
    def decorate(target):
        target.__doc__ = source.__doc__
        return target

    return decorate


class ParserBuffer(Protocol):
    """Protocol used by parsers to read from a bytes buffer."""

    async def get(self, key: Union[int, slice]) -> bytes:
        """Get a range from from the buffer.

        Blocks if the requested range is not available yet. If the requested
        range will never become available (e.g. because it would go past the
        end of file), as much as possible is returned.

        Parameters
        ----------
        key
            Range to return. An integer ``i`` is treated as a single byte range
            ``slice(i, i + 1)``.

        Returns
        -------
        :
            A ``bytes`` object containing the requested range from the buffer.
            This should always be a ``bytes`` objects even if a single integer
            index was provided (this is in contrast to how indexing works on
            ``bytes`` objects). A smaller range than requested may be returned if
            the buffer is unable to provide that range (however, the method must
            block if that range may become available).

        # noqa: DAR202
        """

    def at_eof(self) -> bool:
        """Whether the end of file has been found.

        If the end of file has been found, all possible bytes have been read
        into the buffer and no new bytes will be added.
        """


class BytesBuffer:
    """Implements the `ParserBuffer` protocol for a ``bytes`` object.

    The buffer is static, i.e. all bytes are already provided.

    Parameters
    ----------
    data:
        Data for the buffer.
    """

    def __init__(self, data: bytes):
        self._data = data

    @_copy_doc(ParserBuffer.get)
    async def get(self, key: Union[int, slice]) -> bytes:
        if not isinstance(key, slice):
            key = slice(key, key + 1)
        return self._data[key]

    def at_eof(self) -> bool:
        """Always returns True as the complete buffer is provided at
        construction time."""
        return True


class StreamReaderBuffer:
    """Implements the `ParserBuffer` protocol for a :class:`asyncio.StreamReader`.

    Parameters
    ----------
    reader:
        Reader providing the bytes to be read into the buffer.
    """

    def __init__(self, reader: StreamReader):
        self._reader = reader
        self._buf = bytearray()

    @_copy_doc(ParserBuffer.get)
    async def get(self, key: Union[int, slice]) -> bytes:
        if not isinstance(key, slice):
            key = slice(key, key + 1)

        if key.step is None or key.step > 0:
            max_index = key.stop
        elif key.start is not None:
            max_index = key.start + 1
        else:
            max_index = None

        if max_index is None or max_index < 0:
            self._buf.extend(await self._reader.read())
        elif len(self._buf) <= max_index:
            self._buf.extend(await self._reader.read(max_index - len(self._buf)))

        return self._buf[key]

    async def drop_prefix(self, n: int):
        """Drop the first *n* bytes in the buffer."""
        if len(self._buf) < n:
            await self._reader.readexactly(n - len(self._buf))
            self._buf = bytearray()
        else:
            self._buf = bytearray(self._buf[n:])

    @_copy_doc(ParserBuffer.at_eof)
    def at_eof(self) -> bool:
        return len(self._buf) == 0 and self._reader.at_eof()
