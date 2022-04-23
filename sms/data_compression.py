import binascii
import sys

from romhacking.common import BitArray, RingBuffer, Compression, LZSS


class XOR_SMS(Compression):
    """
        Class to manipulate XOR_SMS Compression

        Games where this compression is found:
            - [SMS] Legend Of Ilusion starring Mickey Mouse
            - [SMS] Ghouls'n Ghosts
            - [SMS] Aventuras da TV Colosso, As
            - [SMS] Michael Jackson's Moonwalker
            - [SMS] Sonic The Hedgehog 2
            - [SMS] Baku Baku
            - [SMS] Batman Returns
            - [SMS] Dynamite Headdy
            - [SMS] Asterix and the Secret Mission
            - [SMS] Sonic Blast
            - [SMS] Deep Duck Trouble Starring Donald Duck
            - [SMS] Sonic Chaos
            - [SMS] Ayrton Senna's Super Monaco GP II
    """

    signature = b'\x5E\x23\x56\x23\x4E\x23\x46\x23\x3E\x20\xF5\xCB\x18\xCB\x19\xCB\x1A\xCB\x1B\x38\x06\xDD\x36\x00\x00'

    def __init__(self, input_data):
        super(XOR_SMS, self).__init__(input_data)

    def decompress(self, *args):
        offset = args[0]
        # Set cursor at compressed data offset
        self.DATA.ENDIAN = "<"
        self.DATA.set_offset(offset)
        self.output = bytearray()
        while True:
            pattern = self.DATA.read_32()
            print(hex(pattern))
            if (pattern & 0x7) == 0:
                break
            else:
                for i in range(32):
                    if pattern & 0x1 == 1:
                        self._output.append(self.DATA.read_8())
                    else:
                        self._output.append(0x00)
                    pattern >>= 1
        return self._output

    def compress(self, *args):
        self.DATA.ENDIAN = "<"
        self.output = bytearray()
        self.temp = bytearray()
        self.encoded = 0
        print(self.DATA.SIZE)
        while self.encoded < self.DATA.SIZE:
            pattern = ''
            for i in range(32):
                value = self.DATA.read_8()
                if value == 0x00:
                    pattern = '0' + pattern
                else:
                    self.temp.append(value)
                    pattern = '1' + pattern
                self.encoded += 1
            pattern = int('0b'+pattern, 2)
            print("0x{:08X}".format(pattern))
            self.output.append(pattern & 0xFF)
            self.output.append((pattern >> 8) & 0xFF)
            self.output.append((pattern >> 16) & 0xFF)
            self.output.append((pattern >> 24) & 0xFF)
            for x in self.temp:
                self.output.append(x)
            self.temp = bytearray()
        return self.output


class LZSIMS(LZSS):
    """
        Class to manipulate LZSIMS Compression

        Games where this compression is found:
            - [SMS] Disney's Alladin
            - [SMS] Master of Darkness
            - [SMS] Masters of Combat
            - [SMS] Ninja Gaiden
    """

    debug = []

    signature = b"\xF5\xCB\x6F\x28\x09\xE6\x07\x47\x7E\x23\x4F\xC3"

    def __init__(self, input_data):
        super(LZSIMS, self).__init__(input_data)

    def lz_unpack(self, temp=0):
        lzpair = self.DATA.read_8()
        position = self._window.CURSOR - ((lzpair >> 4) | temp)
        length = ((lzpair & 0xF) + 2)
        for x in range(length):
            self.append(self._window._buffer[(position+x) & 0x7FF])
        return 1

    def rle_unpack(self, length=0, repetitions=0):
        value = bytearray()
        length += 1
        repetitions += 2
        for x in range(length):
            value += self.DATA.read_8().to_bytes(1, 'big')
        for repeat in range(repetitions):
            for b in value:
                self.append(b)
        return length

    def raw_unpack(self, length=0):
        length += 1
        for x in range(length):
            value = self.DATA.read_8()
            self.append(value)
        return length

    def decompress(self, *args):
        offset = args[0]
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = '<'
        self._window = RingBuffer(0x700, 0x0, 0x0)
        self._output = bytearray()
        size = self.DATA.read_16()-2
        self._decoded = 0
        while self._decoded < size:
            try:
                temp = self.DATA.read_8()
                if not (temp >> 7) & 0x1:
                    #print("LZ: {:02X}".format(temp))
                    self._decoded += self.lz_unpack((temp << 4) & 0xFF0) + 1
                elif not (temp >> 6) & 0x1:
                    #print("RAW: {:02X}".format(temp))
                    self._decoded += self.raw_unpack((temp & 0x3F)) + 1
                elif not (temp >> 5) & 0x1:
                    #print("RLE1: {:02X}".format(temp))
                    self._decoded += self.rle_unpack((temp >> 3)
                                                     & 0x3, (temp & 0x7)) + 1
                else:
                    #print("RLE2: {:02X}".format(temp))
                    repetitions = self.DATA.read_8()
                    self._decoded += self.rle_unpack((temp >> 3)
                                                     & 0x3, repetitions) + 2
            except:
                break

        return self._output

    def compress(self, *args):
        offset = args[0]
        self.DATA.ENDIAN = '<'
        self._window = RingBuffer(0x800, 0x0, 0x0)
        self._buffer = bytearray()
        self._output = bytearray()
        self._output.append(0x0)
        self._output.append(0x0)
        self._encoded = 0
        self.LOOKAHEAD = 0b1111
        self.MIN_LENGTH = 2
        while self._encoded < self.DATA.SIZE:
            # Search for RLE match
            rle_match = self.find_best_rle_match()
            # Search for LZ matches
            lz_match = self.find_best_lz_match(llimit=True)
            # RLE and LZ are less or equal MIN LENGTH, do RAW
            if (
                rle_match[0]*rle_match[1] <= self.MIN_LENGTH
                and lz_match[1] <= self.MIN_LENGTH
            ):
                self.raw_pack(rle_match, lz_match)
            else:
                # LZ are less then MIN LENGTH, do RLE
                if (
                    rle_match[0]*rle_match[1] > self.MIN_LENGTH
                    #and lz_match[1] < self.MIN_LENGTH
                ):
                    self.append_data_rle(self.rle_pack(
                        rle_match, lz_match), rle_match)
                # RLE are less then MIN LENGTH, do LZ
                elif (
                    lz_match[1] > self.MIN_LENGTH
                    and rle_match[0]*rle_match[1] < self.MIN_LENGTH
                ):
                    self.append_data_lz(self.lz_pack(
                        rle_match, lz_match), lz_match)
                else:
                    self.raw_pack(rle_match, lz_match)
        # If RAW in temp buffer, flush then before end
        self.flush_raw(rle_match, lz_match)
        self._output[1] = len(self._output) >> 8
        self._output[0] = len(self._output) & 0xFF
        return self._output

    def append_data_rle(self, data=bytearray(), rle_match=(0, 0)):
        self._output += data
        self.DATA.CURSOR += rle_match[0]*rle_match[1]
        self._encoded += rle_match[0]*rle_match[1]

    def append_data_lz(self, data=bytearray(), lz_match=(0, 0)):
        self._output += data
        self.DATA.CURSOR += lz_match[1]
        self._encoded += lz_match[1]

    def lz_pack(self, rle_match, lz_match):
        if len(self._buffer) > 0:
            self.flush_raw(rle_match, lz_match)
        temp = bytearray()
        try:
            index, length = lz_match
            temp.append((index >> 4) & 0x7F)
            temp.append(((index << 4) & 0xF0) | (((length)-2) & 0xF))
        except:
            pass
        return temp

    def rle_pack(self, rle_match, lz_match):
        if len(self._buffer) > 0:
            self.flush_raw(rle_match, lz_match)
        temp = bytearray()
        _readed = b''
        for i in range(rle_match[0]):
            _readed += self.DATA.read_8().to_bytes(1, 'big')
        self.DATA.CURSOR -= rle_match[0]
        try:
            length = ((rle_match[0]-1) & 0x3) << 3
            if rle_match[1] > 0x7:
                temp.append(0xe0 | length)
                temp.append(rle_match[1]-2)
            else:
                temp.append(
                    0xc0 | length | ((rle_match[1]-2)&0x7))
            for i in range(rle_match[0]):
                temp.append(_readed[i])
        except:
            pass
        return temp

    def raw_pack(self, rle_match, lz_match):
        if len(self._buffer) > 0x3F:
            self.flush_raw(rle_match, lz_match)
        self._buffer.append(self.DATA.read_8())
        self._encoded += 1

    def flush_raw(self, rle_match, lz_match):
        self._output.append(0x80 | ((len(self._buffer)-1) & 0x3F))
        for i in range(len(self._buffer)):
            self._output.append(self._buffer[i])
        self._buffer = bytearray()

    def find_best_rle_match(self):
        _search = bytearray(self.DATA.raw)
        matches = []
        for i in range(self.DATA.SIZE, self.DATA.CURSOR, -1):
            best_repetitions = -1
            best_length = i
            for j in range(0, (self.DATA.SIZE-self._encoded&0x2FE)//best_length, best_length):
                best_repetitions = j//best_length
                total = min(1, best_length*best_repetitions)
                if (not best_length < 1 and not best_repetitions < 2):
                    matches.append((best_length, best_repetitions, total))
                if (
                    _search[self._encoded:self._encoded +
                            best_length] != _search[self._encoded+j:self._encoded+j+best_length]
                ):
                    break
        if len(matches) > 0:
            matches.sort(key=lambda m: m[2])
            matches.reverse()
            best_total = matches[0][2]
            matches = list(filter(lambda m: m[2] == best_total, matches))
            matches.sort(key=lambda m: m[0])
            return (matches[0][0], matches[0][1])
        return (0, 0)
