from asyncio import Future, IncompleteReadError
from unittest.mock import MagicMock

import pytest

from bite.io import BytesBuffer, StreamReaderBuffer
from bite.tests.mock_reader import MockReader


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "index,expected",
    [
        (0, b"0"),
        (2, b"2"),
        (-2, b"8"),
        (slice(3), b"012"),
        (slice(-3), b"0123456"),
        (slice(None, 3), b"012"),
        (slice(2, 5), b"234"),
        (slice(8, None), b"89"),
        (slice(2, 6, 2), b"24"),
        (slice(-8, -4, 2), b"24"),
        (slice(6, 2, -2), b"64"),
        (slice(6, None, -2), b"6420"),
        (slice(None, 2, -2), b"9753"),
        (11, b""),
        (slice(5, 11), b"56789"),
        (slice(11, 12), b""),
        (slice(11, 5, -1), b"9876"),
    ],
)
async def test_stream_reader_buffer_random_access(index, expected):
    buffer = StreamReaderBuffer(MockReader(b"0123456789"))
    assert await buffer.get(index) == expected


@pytest.mark.asyncio
async def test_stream_reader_buffer_reads_not_more_than_necessary():
    future = Future()
    future.set_result(b"abc")

    reader = MagicMock()
    reader.read.return_value = future
    await StreamReaderBuffer(reader).get(slice(0, 3))
    reader.read.assert_called_once_with(3)


@pytest.mark.asyncio
async def test_stream_reader_buffer_repeated_random_access():
    buffer = StreamReaderBuffer(MockReader(b"0123456789"))
    assert await buffer.get(2) == b"2"
    assert await buffer.get(4) == b"4"
    assert await buffer.get(1) == b"1"
    assert await buffer.get(2) == b"2"
    assert await buffer.get(8) == b"8"


@pytest.mark.asyncio
async def test_stream_reader_buffer_get_current():
    buffer = StreamReaderBuffer(MockReader(b"0123456789"))
    await buffer.get(4)
    await buffer.drop_prefix(2)
    await buffer.get(4)
    assert buffer.get_current().startswith(b"2345")


@pytest.mark.asyncio
async def test_stream_reader_buffer_drop_prefix():
    buffer = StreamReaderBuffer(MockReader(b"0123456789"))
    await buffer.get(2)
    await buffer.drop_prefix(4)
    assert await buffer.get(0) == b"4"
    await buffer.drop_prefix(6)
    assert await buffer.get(slice(0, None)) == b""
    assert buffer.at_eof()


@pytest.mark.asyncio
async def test_stream_reader_buffer_cannot_drop_more_than_available():
    buffer = StreamReaderBuffer(MockReader(b"0123456789"))
    with pytest.raises(IncompleteReadError):
        await buffer.drop_prefix(11)


@pytest.mark.asyncio
async def test_stream_reader_buffer_at_eof():
    buffer = StreamReaderBuffer(MockReader(b"0123456789"))
    await buffer.get(9)
    assert not buffer.at_eof()
    await buffer.drop_prefix(10)
    assert await buffer.get(slice(0, 1)) == b""
    assert buffer.at_eof()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "index,expected",
    [
        (0, b"0"),
        (2, b"2"),
        (-2, b"8"),
        (slice(3), b"012"),
        (slice(-3), b"0123456"),
        (slice(None, 3), b"012"),
        (slice(2, 5), b"234"),
        (slice(8, None), b"89"),
        (slice(2, 6, 2), b"24"),
        (slice(-8, -4, 2), b"24"),
        (slice(6, 2, -2), b"64"),
        (slice(6, None, -2), b"6420"),
        (slice(None, 2, -2), b"9753"),
        (11, b""),
        (slice(5, 11), b"56789"),
        (slice(11, 12), b""),
        (slice(11, 5, -1), b"9876"),
    ],
)
async def test_bytes_buffer_random_access(index, expected):
    buffer = BytesBuffer(b"0123456789")
    assert await buffer.get(index) == expected


def test_bytes_buffer_get_current():
    buffer = BytesBuffer(b"0123456789")
    assert buffer.get_current() == b"0123456789"
