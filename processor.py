import struct
from typing import List, Generator

class FastChunkProcessor:
    """High-performance stream byte slice processor using zero-copy memoryviews."""
    __slots__ = ('_buffer', '_view', '_header_fmt', '_header_size')

    def __init__(self, capacity: int = 65536, header_fmt: str = ">I"):
        self._buffer = bytearray(capacity)
        self._view = memoryview(self._buffer)
        self._header_fmt = header_fmt
        self._header_size = struct.calcsize(header_fmt)

    def pack_frames(self, payloads: List[bytes]) -> int:
        """Packs multiple payload chunks directly into contiguous slab without re-allocation."""
        offset = 0
        fmt = self._header_fmt
        hsize = self._header_size
        buf = self._buffer

        for data in payloads:
            dlen = len(data)
            total = hsize + dlen
            if offset + total > len(buf):
                raise ValueError("Slab capacity exceeded during batch pack")
            
            struct.pack_into(fmt, buf, offset, dlen)
            buf[offset + hsize : offset + total] = data
            offset += total

        return offset

    def unpack_stream(self, total_bytes: int) -> Generator[memoryview, None, None]:
        """Zero-copy unpack yielding slice views directly from the active slab buffer."""
        offset = 0
        view = self._view
        fmt = self._header_fmt
        hsize = self._header_size

        while offset < total_bytes:
            dlen = struct.unpack_from(fmt, view, offset)[0]
            start = offset + hsize
            end = start + dlen
            yield view[start:end]
            offset = end

    def process_and_sum_hash(self, total_bytes: int) -> int:
        """Fast accumulative xor checksum directly across memory views."""
        checksum = 0
        for chunk in self.unpack_stream(total_bytes):
            checksum ^= sum(chunk)
        return checksum
