import io
from asyncio import IncompleteReadError


class MockReader:
    """Mocks a :class:`asyncio.StreamReader` with a static ``bytes`` object.

    Parameters
    ----------
    input_buf:
        The input data to provide via the :class:`asyncio.StreamReader` interface.
    """

    def __init__(self, input_buf: bytes):
        self.reader = io.BytesIO(input_buf)
        self.eol_pos = self.reader.seek(0, io.SEEK_END)
        self.read_eol = False
        self.reader.seek(0, io.SEEK_SET)

    async def read(self, n=-1) -> bytes:
        if n < 0 or self.reader.tell() + n > self.eol_pos:
            self.read_eol = True
        return self.reader.read(n)

    async def readline(self) -> bytes:
        return self.reader.readline()

    async def readexactly(self, n) -> bytes:
        buf = await self.read(n)
        if len(buf) < n:
            raise IncompleteReadError(buf, n)
        return buf

    async def readuntil(self, separator=b"\n") -> bytes:
        """Not implemented!"""
        raise NotImplementedError()

    def at_eof(self) -> bool:
        return self.read_eol


__all__ = ["MockReader"]
