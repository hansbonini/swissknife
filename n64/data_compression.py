import struct
import sys
import zlib
import gzip
from romhacking.common import BitArray, RingBuffer, Compression, RLE, LZSS


class LZKONAMI(LZSS):
    """
        Class to manipulate LZKONAMI Compression

        Games where this compression is found:

    """

    def __init__(self, input_data):
        super(LZKONAMI, self).__init__(input_data)

    def decompress(self, offset=0):
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = ">"
        self._window = RingBuffer(0x400, 0x3DF)
        self._output = bytearray()
        compressed_size = self.DATA.read_32()
        _decoded = 0
        start_offset = self.DATA.tell()
        while self.DATA.tell() < (start_offset + compressed_size):
            _readed = self.DATA.read_8()
            if _readed < 0x80:
                # LZ
                length = (_readed >> 2) + 0x2
                offset = ((_readed << 8) | self.DATA.read_8()) & 0x3FF
                _decoded += self.append_from_window(
                    length, self._window.CURSOR-offset)
            elif _readed >= 0x80 and _readed < 0xC0:
                # RAW Copy
                length = (_readed & 0x1F)
                _decoded += self.append_from_data(length)
            elif _readed >= 0xC0 and _readed < 0xE0:
                # RLE
                length = (_readed & 0x1F) + 0x2
                _decoded += self.append_from_data_rle(length)
            elif _readed >= 0xE0 and _readed < 0xFF:
                # RLE Zeros
                length = (_readed & 0x1F) + 0x2
                _decoded += self.append_from_zeroes(length)
            else:
                length = self.DATA.read_8()+0x2
                _decoded += self.append_from_zeroes(length)
        return self._output


class PIC0000(Compression):
    """
        Class to manipulate PIC0000 Compression

        Games where this compression is found:

    """

    def __init__(self, input_data):
        super(PIC0000, self).__init__(input_data)

    def read_header(self):
        current = self.DATA.tell()
        self.DATA.set_offset(current+11)
        width = self.DATA.read_16()
        height = self.DATA.read_16()
        depth = self.DATA.read_16()
        self.DATA.set_offset(current+0x22)
        return (width, height, depth)

    def decompress(self, offset=0):
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = ">"
        self._output = bytearray()
        self._temp = bytearray()
        width,height,depth = self.read_header()
        return self._output
