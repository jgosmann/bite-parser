from asyncio import StreamReader
from typing import Union


class ParserBuffer:
    def __init__(self, reader: StreamReader):
        self._reader = reader
        self._buf = bytearray()

    async def get(self, key: Union[int, slice]) -> bytes:
        if not isinstance(key, slice):
            key = slice(key, key + 1)

        max_index = key.stop if (key.step is None or key.step > 0) else key.start
        if max_index is None or max_index < 0:
            self._buf.extend(await self._reader.read())
        elif len(self._buf) <= max_index:
            self._buf.extend(await self._reader.read(max_index + 1 - len(self._buf)))

        return self._buf[key]
