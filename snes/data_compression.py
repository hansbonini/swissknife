import struct
import sys

from romhacking.common import BitArray, RingBuffer, Compression, RLE, LZSS


class LZKONAMI1(LZSS):
    """
        Class to manipulate LZKONAMI1 Compression

        Games where this compression is found:
        [SNES] The Adventures of Batman & Robin
        [SNES] Teenage Mutant Ninja Turtles IV - Turtles in Time
        [SNES] Biker Mice From Mars 
        [SNES] Contra III-The Alien Wars
        [SNES] Animaniacs
        [SNES] Batman Returns
    """

    def __init__(self, input_data):
        super(LZKONAMI1, self).__init__(input_data)

    def decompress(self, offset=0):
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = "<"
        self._window = RingBuffer(0x400, 0x3DF)
        self._output = bytearray()
        uncompressed_size = self.DATA.read_16()
        print(hex(uncompressed_size))
        terminate = False
        _decoded = 0
        start_offset = self.DATA.tell()
        while (self.DATA.tell() < (start_offset + uncompressed_size)):
            _readed = self.DATA.read_8()
            if _readed < 0x80:
                # LZ
                lzpair = (_readed << 8) | self.DATA.read_8()
                length = ((lzpair >> 10) & 0xFF) + 0x2
                offset = (lzpair & 0x3FF)
                _decoded += self.append_from_window(length, offset)
            elif _readed >= 0x80 and _readed < 0xC0:
                # Block Copy
                length = (_readed & 0x1F)
                _decoded += self.append_from_data(length)
            elif _readed >= 0xC0 and _readed < 0xE0:
                # RLE
                length = (_readed & 0x1F) + 0x2
                _decoded += self.append_from_data_rle(length)
            else:
                # RLE Zeros
                length = (_readed & 0x1F) + 0x2
                _decoded += self.append_from_zeroes(length)
        return self._output


class LZKONAMI2(LZSS):
    """
        Class to manipulate LZKONAMI1 Compression

        Games where this compression is found:
        [SNES] Soreyuke Ebisumaru Karakuri Meiro - Kieta Goemon no Nazo!!
    """

    def __init__(self, input_data):
        super(LZKONAMI2, self).__init__(input_data)

    def decompress(self, offset=0):
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = "<"
        self._window = RingBuffer(0x400, 0x3DF)
        self._output = bytearray()
        uncompressed_size = self.DATA.read_16()
        print(hex(uncompressed_size))
        terminate = False
        _decoded = 0
        start_offset = self.DATA.tell()
        while (self.DATA.tell() < (start_offset + uncompressed_size)):
            _readed = self.DATA.read_8()
            if _readed < 0x80:
                # LZ
                lzpair = (_readed << 8) | self.DATA.read_8()
                length = ((lzpair >> 10) & 0xFF) + 0x2
                offset = (lzpair & 0x3FF)
                _decoded += self.append_from_window(length, offset)
            elif _readed >= 0x80 and _readed < 0xC0:
                # Block Copy
                length = (_readed & 0x1F)
                _decoded += self.append_from_data(length)
            elif _readed >= 0xC0 and _readed < 0xE0:
                # RLE
                length = (_readed & 0x1F) + 0x2
                _decoded += self.append_from_data_rle(length)
            else:
                # RLE Zeros
                if _readed < 0xFF:
                    length = (_readed & 0x1F) + 0x2
                else:
                    length = self.DATA.read_8() + 0x2
                _decoded += self.append_from_zeroes(length)
        return self._output


class LZTOSE(LZSS):
    """
        Class to manipulate LZTOSE Compression

        Games where this compression is found:
        [SNES] Dragon Ball - Super Gokuden
        [SNES] Dragon Ball - Super Butouden 2
        [SNES] Yu Yu Hakusho 2

    """

    def __init__(self, input_data):
        super(LZTOSE, self).__init__(input_data)

    def decompress(self, offset=0):
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = '<'
        self._window = RingBuffer(0x1000, 0, 0x00)
        self._output = bytearray()
        uncompressed_size = self.DATA.read_16()
        print("LEN: {:04X}".format(uncompressed_size))
        _decoded = 0
        while (_decoded < uncompressed_size):
            control = self.DATA.read_8()
            for readed_bits in range(8):
                bit = bool((control >> readed_bits) & 0x1)
                if bit:
                    # RAW
                    _readed = self.DATA.read_8()
                    _decoded += self.append(_readed)
                else:
                    # LZ
                    low, high = self.DATA.read_8(), self.DATA.read_8()
                    print('BYTE:',hex(low), hex(high))
                    length = (low & 0xF) + 3
                    offset = ((high << 8) | low) >> 4
                    print('LZ:', hex(offset), length)
                    _decoded += self.append_from_window(
                        length, self._window.CURSOR-offset)
        return self._output

    def compress(self):
        self.DATA.ENDIAN = '<'
        self._window = RingBuffer(0x1000, 0, 0x00)
        self._buffer = bytearray()
        self._output = bytearray()
        self._output.append(self.DATA.SIZE & 0xFF)
        self._output.append(self.DATA.SIZE >> 8)
        self._encoded = self.DATA.SIZE
        self.LOOKAHEAD = 0b1111
        bitflag = []
        bitcount = 0
        while self._encoded > 0:
            current_offset = self.DATA.CURSOR
            if bitcount > 7:
                bitcount, bitflag = self.write_command_bit(bitcount, bitflag)
            match = self.find_matches()
            if match and match[1] >= 0x3 and self._encoded < self.DATA.SIZE:
                bitflag.append(0)
                (index, length) = match
                relative_index = 0
                while index != self._window.CURSOR:
                    relative_index += 1
                    index += 1
                    index &= self._window.MASK
                _readed = ((relative_index) << 4) | (length-3)
                self._buffer.append(_readed & 0xFF)
                self._buffer.append(_readed >> 8)
                for i in range(0, length):
                    self._window.append(self.DATA.read_8())
                    self._encoded -= 1
            else:
                bitflag.append(1)
                _readed = self.DATA.read_8()
                self._buffer.append(_readed)
                self._window.append(_readed)
                self._encoded -= 1
            bitcount += 1
        bitcount, bitflag = self.write_command_bit(bitcount, bitflag)
        return self._output


class LZSUNSOFT(LZSS):
    """
        Class to manipulate LZSUNSOFT Compression

        Games where this compression is found:
        [SNES] Sugoi Hebereke
        [SNES] Pirates of Dark Water
    """

    def __init__(self, input_data):
        super(LZSUNSOFT, self).__init__(input_data)

    def decompress(self, offset=0):
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = '<'
        self._window = RingBuffer(0x1000, 0xFEE, 0x00)
        self._output = bytearray()
        compressed_size = self.DATA.read_16()
        while (compressed_size > 0):
            control = self.DATA.read_8()
            compressed_size -= 1
            for readed_bits in range(8):
                bit = bool((control >> readed_bits) & 0x1)
                if bit:
                    # RAW
                    _readed = self.DATA.read_8()
                    self.append(_readed)
                    compressed_size -= 1
                else:
                    # LZ
                    low, high = self.DATA.read_8(), self.DATA.read_8()
                    length = (high & 0xF) + 3
                    offset = (low | ((high << 4) & 0xF00))
                    self.append_from_window(
                        length, offset)
                    compressed_size -= 2
        return self._output

    def compress(self):
        self.DATA.ENDIAN = '<'
        self._window = RingBuffer(0x1000, 0xFEE, 0x00)
        self._buffer = bytearray()
        self._output = bytearray()
        self._output.append(0x00)
        self._output.append(0x00)
        self._encoded = 0
        self.LOOKAHEAD = 0b1111
        bitflag = []
        bitcount = 0
        while self._encoded < self.DATA.SIZE:
            current_offset = self.DATA.CURSOR
            if bitcount > 7:
                bitcount, bitflag = self.write_command_bit(bitcount, bitflag)
            match = self.find_matches()
            if match and match[1] >= 0x3 and self._encoded+match[1] < self.DATA.SIZE:
                bitflag.append(0)
                (index, length) = match
                lzpair1 = (index & 0xFF)
                lzpair2 = ((index & 0xF00) >> 4) | (length-3)
                self._buffer.append(lzpair1)
                self._buffer.append(lzpair2)
                for i in range(0, length):
                    self._window.append(self.DATA.read_8())
                    self._encoded += 1
            else:
                bitflag.append(1)
                _readed = self.DATA.read_8()
                self._buffer.append(_readed)
                self._window.append(_readed)
                self._encoded += 1
            bitcount += 1
        compressed_size = len(self._output)-2
        self._output[0] = compressed_size >> 8
        self._output[1] = compressed_size & 0xFF
        return self._output


class LZNATSUME(LZSS):
    """
        Class to manipulate LZNATSUME Compression

        Games where this compression is found:
        [SNES] Ninja Warriors
    """

    def __init__(self, input_data):
        super(LZNATSUME, self).__init__(input_data)

    def decompress(self, offset=0):
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = '<'
        self._window = RingBuffer(0x1000, 0xFEE, 0x00)
        self._output = bytearray()
        self.DATA.read_8()
        uncompressed_size = self.DATA.read_16()
        _decoded = 0
        while (_decoded < uncompressed_size):
            control = self.DATA.read_16()
            for readed_bits in range(16):
                bit = bool((control >> readed_bits) & 0x1)
                if not bit:
                    # RAW
                    _readed = self.DATA.read_8()
                    self.append(_readed)
                    _decoded += 1
                else:
                    # LZ
                    _readed = self.DATA.read_16()
                    print(hex(_readed))
                    offset = _readed & 0x7FF
                    length = (((_readed >> 8) & 0xF8) >> 3)+3
                    print(hex(offset), hex(length))
                    self.append_from_window(
                        length, self._window.CURSOR - offset - 1)
                    _decoded += length
        return self._output

    def compress(self):
        self.DATA.ENDIAN = '<'
        self._window = RingBuffer(0x1000, 0xFEE, 0x00)
        self._buffer = bytearray()
        self._output = bytearray()
        self._output.append(self.DATA.SIZE & 0xFF)
        self._output.append(self.DATA.SIZE >> 8)
        self._encoded = 0
        self.LOOKAHEAD = 0b1111
        bitflag = []
        bitcount = 0
        while self._encoded < self.DATA.SIZE:
            current_offset = self.DATA.CURSOR
            if bitcount > 7:
                bitcount, bitflag = self.write_command_bit(bitcount, bitflag)
            match = self.find_matches()
            if match and match[1] >= 0x3 and self._encoded+match[1] < self.DATA.SIZE:
                bitflag.append(0)
                (index, length) = match
                relative_index = 0
                while index != self._window.CURSOR:
                    relative_index += 1
                    index += 1
                    index &= self._window.MASK
                _readed = ((relative_index) << 4) | (length-3)
                self._buffer.append(_readed & 0xFF)
                self._buffer.append(_readed >> 8)
                for i in range(0, length):
                    self._window.append(self.DATA.read_8())
                    self._encoded += 1
            else:
                bitflag.append(1)
                _readed = self.DATA.read_8()
                self._buffer.append(_readed)
                self._window.append(_readed)
                self._encoded += 1
            bitcount += 1
        return self._output

class LZNAMCO(LZSS):
    """
        Class to manipulate LZNAMCO Compression

        Games where this compression is found:
        [SNES] Pac-Man 2 - The New Adventures
    """

    def __init__(self, input_data):
        super(LZNAMCO, self).__init__(input_data)

    def decompress(self, *args):
        offset = args[0]
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = '<'
        self._output = bytearray()
        _decoded = 0
        while (True):
            control = self.DATA.read_8()
            if control == 0x00:
                break
            length, flag = control >> 1, control &0x1
            if flag == 0:
                for x in range(length):
                    self._output.append(self.DATA.read_8())
                    _decoded+=1
            else:
                _readed = self.DATA.read_8()
                #print(hex(control), hex(_readed))
                index = (_decoded + _readed)&0xFFFF
                if index >= _decoded:
                    index = ((index>>8) | (index<<8))&0xFFFF
                    index -= 1
                    index = ((index>>8) | (index<<8))&0xFFFF
                print(hex(index), hex(length), hex(_decoded))
                for x in range(length):
                    self._output.append(self._output[index])
                    index+=1
                    _decoded+=1
        return self._output

    def compress(self, *args):
        offset = args[0]
        self.DATA.ENDIAN = '<'
        self._window = RingBuffer(0x1000, 0x00, 0x00)
        self._buffer = bytearray()
        self._output = bytearray()
        self._encoded = 0
        self.LOOKAHEAD = 0b1111
        self.MIN_LENGTH = 3
        self.DATA.set_offset(offset)
        while self._encoded < self.DATA.SIZE:
            match=self.find_best_lz_match(llimit=True)
            if match and match[1] >= self.MIN_LENGTH:
                if len (self._buffer) > 0:
                    control = len(self._buffer) << 1
                    control |= 0
                    control &= 0xFF
                    self._output.append(control)
                    for x in self._buffer:
                        self._output.append(x)
                    self._buffer = bytearray()
                index, length = match
                print(hex(index), hex(length), hex(self._encoded))
                for i in range(length):
                    _readed = self.DATA.read_8()
                    self._window.append(_readed)
                index = ((self._encoded-index)-self._encoded) &0xFF
                print(hex((length << 1) | 1), hex(index))
                self._output.append((length << 1) | 1)
                self._output.append(index)
                self._encoded+=length
            else:
                _readed = self.DATA.read_8()
                self._buffer.append(_readed)
                self._window.append(_readed)
                self._encoded+=1
        self._output.append(0x00)
        return self._output


