import struct
import sys

from romhacking.common import BitArray, RingBuffer, Compression, RLE, LZSS

"""
  Games Covered:
        - [SMD] 16 Ton (SegaNet)  
        - [SMD] Alien Storm
        - [SMD] Altered Beast
        - [SMD] Animaniacs
        - [SMD] ATP Tour Championship Tennis  
        - [SMD] Aworg (SegaNet)
        - [SMD] Ayrton Senna's Super Monaco GP II  
        - [SMD] Ball Jacks
        - [SMD] Battletoads
        - [SMD] Beyond Oasis
        - [SMD] Bishoujo Senshi Sailor Moon  
        - [SMD] Buning Force
        - [SMD] Castle of Illusion  
        - [SMD] Castlevania Bloodlines
        - [SMD] Chibi Maruko-Chan: Waku Waku Shopping
        - [SMD] Chou Yakyuu Miracle Nine  
        - [SMD] Classic Collection  
        - [SMD] Columns
        - [SMD] Comix Zone
        - [SMD] Contra: Hard Corps
        - [SMD] Crusader of Centy;
        - [SMD] Dangerous Seed
        - [SMD] Desert Strike: Return to the Gulf
        - [SMD] Disney Collection - Castle of Illusion & Quack Shot  
        - [SMD] Doki Doki Penguin Land MD (SegaNet)
        - [SMD] Dr. Robotinik's Mean Bean Machine
        - [SMD] Dragon Ball Z: Buyuu Retsuden
        - [SMD] Earnest Evans
        - [SMD] El Viento
        - [SMD] Elemental Master
        - [SMD] ESWAT Cyber Police - City Under Siege  
        - [SMD] Fatal Labyrinth
        - [SMD] Final Zone
        - [SMD] Flicky
        - [SMD] Flux for Mega-CD  
        - [SMD] Forgotten Worlds
        - [SMD] Fushigi Umi No Nadia
        - [SMD] Genesis 6-Pak  
        - [SMD] Ghostbusters
        - [SMD] Ghouls n Ghosts
        - [SMD] Golden Axe
        - [SMD] Golden Axe 2
        - [SMD] Golden Axe 3
        - [SMD] Granada
        - [SMD] Hyper Dunk - The Playoff Edition
        - [SMD] J. League Pro Striker - Perfect Edition  
        - [SMD] J. League Pro Striker 2  
        - [SMD] J. League Pro Striker Final Stage  
        - [SMD] Jewel Master
        - [SMD] Jungle Strike
        - [SMD] Klax
        - [SMD] Kyuukai Douchuuki
        - [SMD] Lethal Enforcers
        - [SMD] Lethal Enforcers II - Gun Fighters
        - [SMD] Magical Taruruto-Kun
        - [SMD] Marvel Land 
        - [SMD] Mega Games 10 
        - [SMD] Mega Games 2  
        - [SMD] Mega Games 3  
        - [SMD] Mega Games 6  
        - [SMD] Mega Games 6 (Vol 1) 
        - [SMD] Mega Games 6 (Vol 3) 
        - [SMD] Mega Games I  
        - [SMD] Megapanel
        - [SMD] Mercs
        - [SMD] Metal Fangs  
        - [SMD] Mighty Morphin Power Rangers - The Movie  
        - [SMD] MLBPA Sports Talk Baseball  
        - [SMD] Moonwalker
        - [SMD] Musha
        - [SMD] Pac-Attack
        - [SMD] PacMan2: The New Adventures
        - [SMD] Phantasy Star 2
        - [SMD] Phantasy Star 2 Text Adventures
        - [SMD] Phantasy Star 3
        - [SMD] Phantasy Star 4  
        - [SMD] Phantom 2040  
        - [SMD] Phelios
        - [SMD] Powerball
        - [SMD] Psy-O-Blade
        - [SMD] Pulseman
        - [SMD] Quackshot starring Donald Duck  
        - [SMD] Quad Challenge
        - [SMD] Ranger-X
        - [SMD] Rent A Hero
        - [SMD] Revenge of Shinobi
        - [SMD] Ristar
        - [SMD] Rocket Knight Adventures
        - [SMD] Rolling Thunder 2
        - [SMD] Rolling Thunder 3
        - [SMD] Sega Mega Anser
        - [SMD] Sega Sports 1  
        - [SMD] Sega Top 5  
        - [SMD] Shadow Dancer - The Secret of Shinobi  
        - [SMD] Shinobi III - Return of the Ninja Master  
        - [SMD] Sonic and Knuckles  
        - [SMD] Sonic Classics  
        - [SMD] Sonic Compilation
        - [SMD] Sonic Crackers
        - [SMD] Sonic Eraser
        - [SMD] Sonic The Hedgehog
        - [SMD] Sonic the Hedgehog 2
        - [SMD] Sonic The Hedgehog 3  
        - [SMD] Sparkster
        - [SMD] Splatterhouse 2
        - [SMD] Splatterhouse 3
        - [SMD] Streets of Rage
        - [SMD] Streets of Rage 2
        - [SMD] Streets of Rage 3
        - [SMD] Strider
        - [SMD] Sunset Riders
        - [SMD] Super Hang-On
        - [SMD] Super Monaco GP
        - [SMD] Tecmo Super Bowl II SE  
        - [SMD] Tecmo Super Bowl III Final Edition  
        - [SMD] Teddy Boy Blues (SegaNet)
        - [SMD] Teenage Mutant Ninja Turtles: The Hyperstone Heist
        - [SMD] Teenage Mutant Ninja Turtles: Tournament Fighters
        - [SMD] Tiny Toon Adventures: Acme Allstars
        - [SMD] Tiny Toon Adventures: Buster Hidden Treasure
        - [SMD] Twin Cobra
        - [SMD] Urban Strike
        - [SMD] Virtua Racing  
        - [SMD] Weaponlord
        - [SMD] Wimbledon Championship Tennis  
        - [SMD] World Cup Italia '90
        - [SMD] World of Illusion  
        - [SMD] Wrestle War 
        - [SMD] Zan Yasha Enbuden.
"""


class KOSINSKI(Compression):
    """
        Class to manipulate Kosinski Compression

        Games where this compression is found:
            - [SMD] 16 Ton (SegaNet)  
            - [SMD] Aworg (SegaNet) 
            - [SMD] Ayrton Senna's Super Monaco GP II  
            - [SMD] Battletoads
            - [SMD] Bishoujo Senshi Sailor Moon  
            - [SMD] Disney Collection - Castle of Illusion & Quack Shot  
            - [SMD] Doki Doki Penguin Land MD (SegaNet)
            - [SMD] Flux for Mega-CD  
            - [SMD] Genesis 6-Pak  
            - [SMD] J. League Pro Striker - Perfect Edition  
            - [SMD] J. League Pro Striker 2  
            - [SMD] J. League Pro Striker Final Stage  
            - [SMD] Mega Games 10
            - [SMD] Mega Games 2  
            - [SMD] Mega Games 3  
            - [SMD] Mega Games 6 (Vol 1) 
            - [SMD] Mega Games 6 (Vol 3) 
            - [SMD] Phantasy Star 4  
            - [SMD] Phantom 2040  
            - [SMD] Quackshot starring Donald Duck
            - [SMD] Shinobi III - Return of the Ninja Master  
            - [SMD] Sonic and Knuckles
            - [SMD] Sonic Classics 
            - [SMD] Sonic Crackers
            - [SMD] Sonic The Hedgehog
            - [SMD] Sonic The Hedgehog 2
            - [SMD] Sonic The Hedgehog 3  
            - [SMD] Streets of Rage
            - [SMD] Streets of Rage 3  
            - [SMD] Teddy Boy Blues (SegaNet)
            - [SMD] Virtua Racing  
            - [SMD] World of Illusion
    """

    signature = b'\x55\x8F\x1F\x58\x00\x01\x1E\x98\x3A\x17\x78\x0F\xE2\x4D\x40\xC6'
    signature += b'\x51\xCC\x00\x0C\x1F\x58\x00\x01\x1E\x98\x3A\x17\x78\x0F\x44\xC6'
    signature += b'\x64\x04\x12\xD8\x60\xE6\x76\x00\xE2\x4D\x40\xC6\x51\xCC\x00\x0C'
    signature += b'\x1F\x58\x00\x01\x1E\x98\x3A\x17\x78\x0F\x44\xC6\x65\x2C\xE2\x4D'

    def __init__(self, input_data):
        super(KOSINSKI, self).__init__(input_data)

    def get_bitflag(self, control, readed_bits):
        bit = bool(control & (1 << readed_bits))
        readed_bits += 1
        # If entire control word is readed as bit
        # set new control word
        if readed_bits >= 16:
            control, readed_bits = self.read_control_word()
        return control, readed_bits, bit

    def read_control_word(self):
        control = self.DATA.read_16()
        readed_bits = 0
        return control, readed_bits

    def decompress(self, *args):
        offset = args[0]
        # Set cursor at compressed data offset
        self.DATA.set_offset(offset)
        # Set to native endian
        self.DATA.ENDIAN = '@'
        # Read control word to use as bit flags
        control = self.DATA.read_16()
        # Set number of bits readed to 0
        readed_bits = 0
        # Set output _buffer as empty bytearray
        self._output = bytearray()
        # Iterate over control flags
        while True:
            control, readed_bits, bit = self.get_bitflag(control, readed_bits)
            # flag is set
            # get uncompressed byte
            if bit:
                self._output.append(self.DATA.read_8())
            # if flag is not set, do decompression
            else:
                control, readed_bits, bit = self.get_bitflag(
                    control, readed_bits)
                # if flag is set
                # get count and offset parameters
                # uncompressed as byte
                if bit:
                    low, high = self.DATA.read_8(), self.DATA.read_8()
                    count = high & 0x7
                    # if count is 0 read more 1 byte
                    if count == 0:
                        count = self.DATA.read_8()
                        if count == 0:
                            break
                        if count == 1:
                            continue
                    # if not increment count
                    else:
                        count += 1
                    offset = 0x2000 - (((0xF8 & high) << 5) | low)
                # if not
                # get count parameter compressed as bit flag
                # and offset parameter uncompressed as byte
                else:
                    control, readed_bits, bit = self.get_bitflag(
                        control, readed_bits)
                    low = 1 if bit else 0
                    control, readed_bits, bit = self.get_bitflag(
                        control, readed_bits)
                    high = 1 if bit else 0
                    count = low*2 + high + 1
                    offset = 0x100 - self.DATA.read_8()
                # iterate over count pattern
                # and copy byte at offset position
                # to the end of _output
                for _ in range(count+1):
                    self._output.append(self._output[-offset])
        return self._output


class NEMESIS(Compression):
    """
        Class to manipulate Nemesis Compression

        Games where this compression is found:
            - [SMD] Alien Storm  
            - [SMD] ATP Tour Championship Tennis  
            - [SMD] Ayrton Senna's Super Monaco GP II  
            - [SMD] Castle of Illusion  
            - [SMD] Chou Yakyuu Miracle Nine  
            - [SMD] Classic Collection  
            - [SMD] Columns
            - [SMD] Disney Collection - Castle of Illusion & Quack Shot  
            - [SMD] Dr. Robotinik's Mean Bean Machine
            - [SMD] ESWAT Cyber Police - City Under Siege  
            - [SMD] Fatal Labyrinth
            - [SMD] Flicky
            - [SMD] Forgotten Worlds
            - [SMD] Genesis 6-Pak  
            - [SMD] Ghostbusters
            - [SMD] Ghouls n Ghosts
            - [SMD] Golden Axe
            - [SMD] Golden Axe 2
            - [SMD] Golden Axe 3
            - [SMD] Jewel Master
            - [SMD] Magical Taruruto-Kun
            - [SMD] Mega Games 10 
            - [SMD] Mega Games 2  
            - [SMD] Mega Games 3  
            - [SMD] Mega Games 6  
            - [SMD] Mega Games 6  
            - [SMD] Mega Games 6  
            - [SMD] Mega Games I  
            - [SMD] Mercs
            - [SMD] Metal Fangs  
            - [SMD] Mighty Morphin Power Rangers - The Movie  
            - [SMD] MLBPA Sports Talk Baseball  
            - [SMD] Moonwalker
            - [SMD] Musha
            - [SMD] Phantasy Star 2
            - [SMD] Phantasy Star 2 Text Adventures
            - [SMD] Phantasy Star 3
            - [SMD] Phantasy Star 4
            - [SMD] Psy-O-Blade
            - [SMD] Pulseman
            - [SMD] Quackshot starring Donald Duck  
            - [SMD] Rent A Hero
            - [SMD] Revenge of Shinobi
            - [SMD] Ristar
            - [SMD] Sega Mega Anser
            - [SMD] Sega Sports 1  
            - [SMD] Sega Top 5  
            - [SMD] Shadow Dancer - The Secret of Shinobi  
            - [SMD] Sonic and Knuckles  
            - [SMD] Sonic Classics  
            - [SMD] Sonic Compilation
            - [SMD] Sonic Crackers
            - [SMD] Sonic Eraser
            - [SMD] Sonic The Hedgehog
            - [SMD] Sonic the Hedgehog 2
            - [SMD] Sonic the Hedgehog 3
            - [SMD] Streets of Rage
            - [SMD] Streets of Rage 2
            - [SMD] Streets of Rage 3
            - [SMD] Strider
            - [SMD] Super Hang-On
            - [SMD] Super Monaco GP
            - [SMD] Tecmo Super Bowl II SE  
            - [SMD] Tecmo Super Bowl III Final Edition  
            - [SMD] Twin Cobra
            - [SMD] Virtua Racing  
            - [SMD] Wimbledon Championship Tennis  
            - [SMD] World Cup Italia '90
            - [SMD] World of Illusion  
            - [SMD] Wrestle War  
    """

    signature = b'\x3E\x06\x51\x47\x32\x05\xEE\x69\x0C\x01\x00\xFC\x64\x3E\x02\x41'
    signature += b'\x00\xFF\xD2\x41\x10\x31\x10\x00\x48\x80\x9C\x40\x0C\x46\x00\x09'
    signature += b'\x64\x06\x50\x46\xE1\x45\x1A\x18\x12\x31\x10\x01\x30\x01\x02\x41'
    signature += b'\x00\x0F\x02\x40\x00\xF0\xE8\x48\xE9\x8C\x88\x01\x53\x43\x66\x06'

    def __init__(self, input_data):
        super(NEMESIS, self).__init__(input_data)

    def decompress(self, *args):
        offset = args[0]
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = '>'
        xored, tiles = divmod(self.DATA.read_16(), 0x8000)
        # Stage 1
        _window = [0x01]*0x200
        _readed = self.DATA.read_8()
        while _readed != 0xFF:
            if _readed > 0x7F:
                pattern, _readed = _readed, self.DATA.read_8()
            length = 0x8 - (_readed & 0xF)
            _readed = ((_readed & 0xF0) >> 4) | ((_readed & 0xF) << 4)
            pattern = (pattern & 0xF) | (_readed << 4)
            offset = self.DATA.read_8() * (1 << (length+1))
            if (offset >= 0x200):
                exit(0)
            length = 1 << length
            for i in range(length):
                _window = _window[:offset] + \
                    [pattern >> 8, pattern] + _window[offset+2:]
                offset += 2
            _readed = self.DATA.read_8()
        # Stage 2
        modulation = 0x10
        length = 0
        xor_pattern = 0
        _readed = self.DATA.read_16()
        for i in range(tiles):
            for j in range(8):
                pattern = 0
                for k in range(8):
                    length -= 1
                    if length == -1:
                        mode = _readed // (1 << (modulation - 8))
                        if (mode & 0xFF) >= 0xFC:
                            if modulation < 0xF:
                                modulation += 8
                                _readed = ((_readed << 8) |
                                           self.DATA.read_8()) & 0xFFFF
                            modulation -= 0xD
                            length = (
                                (_readed // (1 << modulation)) & 0x70) >> 4
                            next_pattern = (_readed // (1 << modulation)) & 0xF
                        else:
                            cursor = (mode & 0xFF) * 2
                            modulation -= _window[cursor]
                            length = (_window[cursor+1] & 0xF0) >> 4
                            next_pattern = _window[cursor+1] & 0xF
                        if modulation < 9:
                            modulation += 8
                            _readed = ((_readed << 8) |
                                       self.DATA.read_8()) & 0xFFFF
                    pattern = ((pattern << 4) | next_pattern) & 0xFFFFFFFF
                if xored:
                    xor_pattern = xor_pattern ^ pattern
                    self._output.append(xor_pattern >> 24)
                    self._output.append((xor_pattern >> 16) & 0xFF)
                    self._output.append((xor_pattern >> 8) & 0xFF)
                    self._output.append(xor_pattern & 0xFF)
                else:
                    self._output.append(pattern >> 24)
                    self._output.append((pattern >> 16) & 0xFF)
                    self._output.append((pattern >> 8) & 0xFF)
                    self._output.append(pattern & 0xFF)
        return self._output


class ENIGMA(Compression):

    signature = b'\x70\x07\x3E\x06\x9E\x40\x32\x05\xEE\x69\x02\x41\x00\x7F\x34\x01'
    signature += b'\x0C\x41\x00\x40\x64\x04\x70\x06\xE2\x4A'

    def __init__(self, input_data):
        super(ENIGMA, self).__init__(input_data)


class SAXMAN(Compression):
    def __init__(self, input_data):
        super(SAXMAN, self).__init__(input_data)


class XOR_SEGARD(Compression):
    """
        Class to manipulate XOR_SEGARD Compression

        Games where this compression is found:
            - [SMD] Alex Kidd in Enchanted Castle
            - [SMD] Altered Beast
            - [SMD] Columns
            - [SMD] Golden Axe
            - [SMD] Hokuto no Ken: Shin Seikimatsu Kyuuseishu Densetsu
            - [SMD] Last Battle
            - [SMD] Osomatsu-kun - Hachamecha Gekijou
            - [SMD] World Championship Soccer

    """

    signature = b'\x70\x00\x74\x00\x14\x18\x67\x30\x6B\x52\x53\x42\x24\x4C\x16\x18'
    signature += b'\x18\x18\xE1\x4C\x18\x18\x48\x44\x18\x18\xE1\x4C\x18\x18\x80\x84'
    signature += b'\x7E\x1F\xE3\x8C\x64\x02\x14\x83\x52\x4A\x51\xCF\xFF\xF6\x51\xCA'
    signature += b'\xFF\xDC\x72\xFF\xB1\x81\x67\x10\x26\x4C\x7E\x1F\xD0\x80\x65\x02'
    signature += b'\x16\x98\x52\x4B\x51\xCF\xFF\xF6\x2C\x4C\x2A\x9E\x2A\x9E\x2A\x9E'

    def __init__(self, input_data):
        super(XOR_SEGARD, self).__init__(input_data)

    def decompress(self, *args):
        offset = args[0]
        # Set cursor at compressed data offset
        self.DATA.ENDIAN = ">"
        self.DATA.set_offset(offset)
        _window = bytearray([0x00]*32)
        _readed = self.DATA.read_8()

        while _readed != 0xFF:
            cursor = 0
            pattern = 0
            for _ in range(_readed):
                a = self.DATA.read_8()
                b = self.DATA.read_32()
                pattern |= b
                for i in range(0x20):
                    b <<= 1
                    cb = divmod(b, 0xFFFFFFFF)[0]  # get carry bit of bitshift
                    bit = bool(cb & 0x1)
                    if bit:
                        _window[i] = a
                    else:
                        pass
            cursor = 0
            pattern2 = 0xFFFFFFFF ^ pattern
            if pattern2 != 0:
                for _ in range(0x20):
                    pattern += pattern
                    cb = divmod(pattern, 0xFFFFFFFF)[0]
                    bit = bool(cb & 0x1)
                    if bit == 1:
                        cursor += 1
                    else:
                        _window[cursor] = self.DATA.read_8()
                        cursor += 1
            for i in range(len(_window)):
                self._output.append(_window[i])
            _readed = self.DATA.read_8()
        return self._output


class LZSTI(LZSS):
    """
        Class to manipulate LZSTI Compression

        Games where this compression is found:
            - [SMD] Comix Zone
    """

    signature = b'\x43\xF9\xFF\xFF\x4E\x34\x40\xE7\x00\x7C\x07\x00\x3A\x00\x36\x41'
    signature += b'\x3C\x18\x3E\x18\x53\x46\x53\x47\x61\x00\xFE\x72\xE2\x4B\x53\x43'
    signature += b'\x24\x49\x78\x00\x38\x05\xE5\x8C\xE4\x4C\x00\x44\x40\x00\x48\x44'
    signature += b'\x28\x84\x38\x06\x3F\x07\x3E'

    def __init__(self, input_data):
        super(LZSTI, self).__init__(input_data)

    def decompress(self, *args):
        offset = args[0]
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = '>'
        self._window = RingBuffer(0x400, 0x00, 0x00)
        self._output = bytearray()
        uncompressed_size = self.DATA.read_16()
        bitstream = BitArray(self.DATA.read())
        _decoded = 0
        while (_decoded < uncompressed_size):
            bit = bool(bitstream.read_int(1))
            if bit:
                _readed = bitstream.read_int(8)
                _decoded += self.append(_readed)
            else:
                offset = bitstream.read_int(10)
                length = bitstream.read_int(4) + 2
                _decoded += self.append_from_window(length, offset)
        return self._output


class LZSTI2(LZSS):
    """
        Class to manipulate LZSTI2 Compression

        Games where this compression is found:
            - [SMD] Kid Chameleon
    """
    signature = b'\xBE\x4A\x63\x4C\x60\x00\x01\x54\xE7\x49\x3C\x01\xCC\x44\x1C\x19'
    signature += b'\x9D\xC6\xD2\x01\x65\x06\xD2\x01\x65\x18\x60\x18\xD2\x01\x64\x10'

    def __init__(self, input_data):
        super(LZSTI2, self).__init__(input_data)


class LZHWESTONE(Compression):
    """
        Class to manipulate LZHWESTONE Compression

        Games where this compression is found:
            - [SMD] Kid Chameleon
    """

    signature = b'\x12\x18\x14\x18\xE1\x4A\x14\x18\x48\x42\x14\x18\xE1\x4A\x14\x18'
    signature += b'\x86\x82\x24'

    def __init__(self, input_data):
        super(LZHWESTONE, self).__init__(input_data)


class LZSILICONSYNAPSE(LZSS):
    """
        Class to manipulate LZSILICONSYNAPSE Compression

        Games where this compression is found:
            - [SMD] Boogerman
            - [SMD] Death and Return of Superman
            - [SMD] Rock n Roll Racing
            - [SMD] The Lost Vikings
    """
    signature = b'\x12\x18\x14\xC1\xE1\x46\x1C\x01\xE3'

    def __init__(self, input_data):
        super(LZSILICONSYNAPSE, self).__init__(input_data)


class LZNAMCO(LZSS):
    """
        Class to manipulate LZNAMCO Compression

        Games where this compression is found:
            - [SMD] Ball Jacks
            - [SMD] Buning Force
            - [SMD] Chibi Maruko-Chan: Waku Waku Shopping
            - [SMD] Fushigi Umi No Nadia
            - [SMD] Klax
            - [SMD] Kyuukai Douchuuki
            - [SMD] Marvel Land 
            - [SMD] Megapanel
            - [SMD] Pac-Attack
            - [SMD] PacMan2: The New Adventures
            - [SMD] Phelios
            - [SMD] Powerball
            - [SMD] Rolling Thunder 2
    """

    signature = b'\x18\x18\x12\x18\x36\x01'

    def __init__(self, input_data):
        super(LZNAMCO, self).__init__(input_data)

    def decompress(self, *args):
        offset = args[0]
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = '>'
        self._window = RingBuffer(0x1000, 0xFEE, 0x00)
        self._output = bytearray()
        uncompressed_size = self.DATA.read_16()
        _decoded = 0
        while (_decoded < uncompressed_size):
            control = self.DATA.read_8()
            for readed_bits in range(8):
                bit = bool((control >> readed_bits) & 0x1)
                if bit:
                    _readed = self.DATA.read_8()
                    self.append(_readed)
                    _decoded += 1
                else:
                    try:
                        _readed = self.DATA.read_16()
                    except:
                        break
                    length = (_readed & 0xF) + 3
                    offset = ((_readed & 0xF0) << 4) | (_readed >> 8)
                    self.append_from_window(length, offset)
                    _decoded += length
        return self._output

    def compress(self):
        self.DATA.ENDIAN = '>'
        self._window = RingBuffer(0x1000, 0xFEE, 0x00)
        self._buffer = bytearray()
        self._output = bytearray()
        self._output.append(self.DATA.SIZE >> 8)
        self._output.append(self.DATA.SIZE & 0xFF)
        self._encoded = 0
        self.LOOKAHEAD = 0b1111
        self.MIN_LENGTH = 3
        bitflag = []
        bitcount = 0
        while self._encoded < self.DATA.SIZE:
            current_offset = self.DATA.CURSOR
            if bitcount > 7:
                bitcount, bitflag = self.write_command_bit(bitcount, bitflag)
            match = self.find_best_lz_match()
            if match and match[1] >= self.MIN_LENGTH and (self.DATA.SIZE-self._encoded) > 7:
                bitflag.append(0)
                (index, length) = match
                offset = (self._window.CURSOR -
                          index) % self._window.MAX_WINDOW_SIZE
                _readed = ((offset << 8) & 0xFF00) | ((offset >> 4) & 0xF0)
                _readed &= 0xFFF0
                _readed |= (length-3)
                self._buffer.append(_readed >> 8)
                self._buffer.append(_readed & 0xFF)
                for i in range(0, length):
                    self.DATA.read_8()
                self._encoded += length
            else:
                bitflag.append(1)
                _readed = self.DATA.read_8()
                self._buffer.append(_readed)
                self._encoded += 1
            bitcount += 1
        if bitcount > 0:
            bitcount, bitflag = self.write_command_bit(bitcount, bitflag)
        return self._output


class LZTECHNOSOFT(LZSS):
    """
        Class to manipulate LZTECHNOSOFT Compression

        Games where this compression is found:
            - [SMD] Elemental Master
    """

    signature = b'\x55\x87\x12\x18\x10\x18\x2A\x00\xC0\x7C\x00\xF0\xE9\x40\x80\x41'

    def __init__(self, input_data):
        super(LZTECHNOSOFT, self).__init__(input_data)

    def decompress(self, *args):
        offset = args[0]
        size = args[1]
        self.DATA.ENDIAN = '>'
        self._window = RingBuffer(0x1000, 0xFEE, 0x00)
        self._output = bytearray()
        self.DATA.set_offset(offset)
        _decoded = 0
        while (_decoded < size):
            control = self.DATA.read_8()
            _decoded += 1
            for readed_bits in range(8):
                bit = bool((control >> readed_bits) & 0x1)
                if bit:
                    _readed = self.DATA.read_8()
                    self.append(_readed)
                    _decoded += 1
                else:
                    _readed = self.DATA.read_16()
                    length = (_readed & 0xF) + 3
                    offset = ((_readed & 0xF0) << 4) | (_readed >> 8)
                    self.append_from_window(length, offset)
                    _decoded += 2
        return self._output

    def compress(self):
        self.DATA.ENDIAN = '>'
        self._window = RingBuffer(0x1000, 0xFEE, 0x00)
        self._buffer = bytearray()
        self._output = bytearray()
        self._encoded = 0
        self.LOOKAHEAD = 0b1111
        self.MIN_LENGTH = 3
        bitflag = []
        bitcount = 0
        while self._encoded < self.DATA.SIZE:
            current_offset = self.DATA.CURSOR
            if bitcount > 7:
                bitcount, bitflag = self.write_command_bit(bitcount, bitflag)
            match = self.find_best_lz_match()
            if match and match[1] >= self.MIN_LENGTH and (self.DATA.SIZE-self._encoded) > 7:
                bitflag.append(0)
                (index, length) = match
                offset = (self._window.CURSOR -
                          index) % self._window.MAX_WINDOW_SIZE
                _readed = ((offset << 8) & 0xFF00) | ((offset >> 4) & 0xF0)
                _readed &= 0xFFF0
                _readed |= (length-self.MIN_LENGTH)
                self._buffer.append(_readed >> 8)
                self._buffer.append(_readed & 0xFF)
                for i in range(0, length):
                    self.DATA.read_8()
                self._encoded += length
            else:
                bitflag.append(1)
                _readed = self.DATA.read_8()
                self._buffer.append(_readed)
                self._encoded += 1
            bitcount += 1
        if bitcount > 0:
            bitcount, bitflag = self.write_command_bit(bitcount, bitflag)
        return self._output


class LZKONAMI1(LZSS):
    """
        Class to manipulate LZKONAMI1 Compression

        Games where this compression is found:
            - [SMD] Animaniacs
            - [SMD] Contra: Hard Corps
            - [SMD] Lethal Enforcers II - Gun Fighters
            - [SMD] Sparkster
    """

    def __init__(self, input_data):
        super(LZKONAMI1, self).__init__(input_data)

    def decompress(self, *args):
        offset = args[0]
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = ">"
        self._window = RingBuffer(0x400, 0x3C0, 0x20)
        self._output = bytearray()
        uncompressed_size = self.DATA.read_16()
        _decoded = 0
        while (_decoded < uncompressed_size):
            control = self.DATA.read_8()
            for readed_bits in range(8):
                bit = bool((control >> readed_bits) & 0x1)
                _readed = self.DATA.read_8()
                if bit:
                    if _readed == 0x1F:
                        break
                    elif _readed > 0x80:
                        length = (_readed & 0x1F) + 3
                        offset = ((_readed << 3) & 0xFF00) | self.DATA.read_8()
                        _decoded += self.append_from_window(length, offset)
                    elif _readed >= 0x80 and _readed <= 0xC0:
                        length = (_readed >> 4) - 6
                        offset = (self._window.CURSOR-(_readed & 0xF))
                        _decoded += self.append_from_window(length, offset)
                    elif _readed >= 0xC0:
                        length = _readed - 0xB8
                        _decoded += self.append_from_data(length)
                else:
                    _decoded += self.append(_readed)
        return self._output


class LZKONAMI2(LZSS):
    """
        Class to manipulate LZKONAMI2 Compression

        Games where this compression is found:
            - [SMD] Animaniacs
            - [SMD] Castlevania Bloodlines
            - [SMD] Contra: Hard Corps
            - [SMD] Rocket Knight Adventures
            - [SMD] Sunset Riders
            - [SMD] Teenage Mutant Ninja Turtles: The Hyperstone Heist
            - [SMD] Tiny Toon Adventures: Acme Allstars
            - [SMD] Tiny Toon Adventures: Buster Hidden Treasure
    """

    def __init__(self, input_data):
        super(LZKONAMI2, self).__init__(input_data)

    def decompress(self, *args):
        offset = args[0]
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = ">"
        self._window = RingBuffer(0x400, 0x3C0, 0x20)
        self._output = bytearray()
        compressed_size = offset+self.DATA.read_16()
        _decoded = 0
        while self.DATA.tell() < compressed_size:
            control = self.DATA.read_8()
            for readed_bits in range(8):
                bit = bool((control >> readed_bits) & 0x1)
                if bit:
                    _readed = self.DATA.read_8()
                    _decoded += self.append(_readed)
                else:
                    _readed = self.DATA.read_16()
                    length = ((_readed & 0xFC00) >> 10) + 1
                    offset = _readed
                    _decoded += self.append_from_window(length, offset)
        return self._output


class LZKONAMI3(LZSS):
    """
        Class to manipulate LZKONAMI3 Compression

        Games where this compression is found:
            - [SMD] Castlevania Bloodlines
            - [SMD] Hyper Dunk - The Playoff Edition
            - [SMD] Lethal Enforcers
            - [SMD] Teenage Mutant Ninja Turtles: Tournament Fighters
            - [SMD] Tiny Toon Adventures: Acme Allstars
    """

    signature = b'\x14\x00\xE8\x4A\x02\x42\x00\x03\x52\x42\x02'

    def __init__(self, input_data):
        super(LZKONAMI3, self).__init__(input_data)

    def decompress(self, *args):
        offset = args[0]
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = ">"
        self._window = RingBuffer(0x400, 0x3DF)
        self._output = bytearray()
        uncompressed_size = self.DATA.read_16()
        terminate = False
        _decoded = 0
        while (_decoded < uncompressed_size) and (terminate == False):
            control = self.DATA.read_8()
            for readed_bits in range(8):
                bit = bool((control >> readed_bits) & 0x1)
                _readed = self.DATA.read_8()
                if bit:
                    if _readed == 0x1F:
                        terminate = True
                    elif _readed < 0x80:
                        length = (_readed & 0x1F) + 3
                        offset = ((_readed & 0x60) << 3) | self.DATA.read_8()
                        _decoded += self.append_from_window(length, offset)
                    elif _readed >= 0x80 and _readed <= 0xC0:
                        length = ((_readed >> 4) & 0x3) + 2
                        offset = (self._window.CURSOR-(_readed & 0xF))
                        _decoded += self.append_from_window(length, offset)
                    else:
                        length = (_readed & 0x3F) + 8
                        _decoded += self.append_from_data(length)
                else:
                    _decoded += self.append(_readed)
        return self._output


class LZTOSE(LZSS):
    """
        Class to manipulate LZTOSE Compression

        Games where this compression is found:
            - [SMD] Dragon Ball Z: Buyuu Retsuden
    """

    signature = b'\x16\x30\x10\x04\x18\x03\x02\x44\x00\x0F\xB8\x02\x67\x1E\x14\x04'
    signature += b'\x48\xE7\xF0\xC0\xD8\x44\x41\xFA\x07\x3C\xD0\xC4\xD0\xD0\x43\xF9'
    signature += b'\xFF\xFF\x20\x00\x4E\xBA\xF7\x52\x4C\xDF\x03\x0F\x38\x30\x10\x04'
    signature += b'\x02\x43\x00\xF0\xE6'

    def __init__(self, input_data):
        super(LZTOSE, self).__init__(input_data)

    def decompress(self, *args):
        offset = args[0]
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = '>'
        self._window = RingBuffer(0x2000, 0x00, 0x00)
        self._output = bytearray()
        low, high = self.DATA.read_8(), self.DATA.read_8()
        uncompressed_size = (((high << 8) | low) & 0x7FFF) + 1
        _decoded = 0
        while (_decoded < uncompressed_size):
            try:
                control = self.DATA.read_8()
                for readed_bits in range(8):
                    bit = bool((control >> readed_bits) & 0x1)
                    if bit:
                        _readed = self.DATA.read_8()
                        _decoded += self.append(_readed)
                    else:
                        low, high = self.DATA.read_8(), self.DATA.read_8()
                        length = (low & 0xF) + 3
                        offset = ((high << 8) | low) >> 4
                        _decoded += self.append_from_window(
                            length, self._window.CURSOR-offset)
            except:
                break
        return self._output[0:uncompressed_size]

    def compress(self):
        self.DATA.ENDIAN = '>'
        self._window = RingBuffer(0x1000, 0x00, 0x00)
        self._buffer = bytearray()
        self._output = bytearray()
        self._output.append(self.DATA.SIZE-1 & 0xFF)
        self._output.append(self.DATA.SIZE-1 >> 8)
        self._encoded = 0
        self.LOOKAHEAD = 0b1111
        self.MIN_LENGTH = 3
        bitflag = []
        bitcount = 0
        while self._encoded < self.DATA.SIZE:
            current_offset = self.DATA.CURSOR
            if bitcount > 7:
                bitcount, bitflag = self.write_command_bit(bitcount, bitflag)
            match = self.find_best_lz_match(llimit=True)
            if match and match[1] >= self.MIN_LENGTH:
                bitflag.append(0)
                (index, length) = match
                _readed = (index & self._window.MASK) << 4
                _readed &= 0xFFF0
                _readed |= (length-3)
                self._buffer.append(_readed & 0xFF)
                self._buffer.append(_readed >> 8)
                for i in range(0, length):
                    self.DATA.read_8()
                self._encoded += length
            else:
                bitflag.append(1)
                _readed = self.DATA.read_8()
                self._buffer.append(_readed)
                self._encoded += 1
            bitcount += 1
        if bitcount > 0:
            bitcount, bitflag = self.write_command_bit(bitcount, bitflag)
        return self._output


class LZSTRIKE(LZSS):
    """
        Class to manipulate LZNAMCO Compression

        Games where this compression is found:
            - [SMD] Desert Strike: Return to the Gulf
            - [SMD] Jungle Strike
            - [SMD] Urban Strike
    """

    def __init__(self, input_data):
        super(LZSTRIKE, self).__init__(input_data)

    def decompress(self, *args):
        offset = args[0]
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = '>'
        self._window = RingBuffer(0x800, 0x7EE, 0x00)
        self._output = bytearray()
        uncompressed_size = self.DATA.read_16()
        _decoded = 0
        while (_decoded < uncompressed_size):
            control = self.DATA.read_8()
            for readed_bits in range(8):
                bit = bool((control >> readed_bits) & 0x1)
                if bit:
                    _readed = self.DATA.read_8()
                    _decoded += self.append(_readed)
                else:
                    _readed = self.DATA.read_16()
                    length = (_readed & 0xF) + 3
                    offset = ((_readed & 0xF0) << 4) | (_readed >> 8)
                    _decoded += self.append_from_window(length, offset)
        return self._output


class LZNEXTECH(LZSS):
    """
        Class to manipulate LZNEXTECH Compression

        Games where this compression is found:
            - [SMD] Crusader of Centy;
    """

    def __init__(self, input_data):
        super(LZNEXTECH, self).__init__(input_data)

    def init_window(self):
        for i in range(0x100):
            for j in range(0x0D):
                self._window._buffer[i * 0x0D + j] = i
            self._window._buffer[0xD00+i] = i
            self._window._buffer[0xE00+i] = 0xFF - i
            if i < 0x80:
                self._window._buffer[0xF00+i] = 0x00
            if i < 0x6E:
                self._window._buffer[i] = 0x20
            self._window.CURSOR = 0xFEE

    def decompress(self, *args):
        offset = args[0]
        self.DATA.set_offset(offset)
        self.DATA.ENDIAN = '<'
        self._window = RingBuffer(0x1000, 0xFEE, 0x00)
        self._output = bytearray()
        compressed_size = self.DATA.read_32()
        uncompressed_size = self.DATA.read_32()
        _decoded = 0
        self.DATA.ENDIAN = '>'
        self.init_window()
        while (_decoded < uncompressed_size):
            control = self.DATA.read_8()
            for readed_bits in range(8):
                bit = bool((control >> readed_bits) & 0x1)
                if bit:
                    _readed = self.DATA.read_8()
                    _decoded += self.append(_readed)
                else:
                    _readed = self.DATA.read_16()
                    length = (_readed & 0xF) + 3
                    offset = ((_readed & 0xF0) << 4) | (_readed >> 8)
                    _decoded += self.append_from_window(length, offset)
        return self._output


class LZWOLFTEAM(LZNEXTECH):
    """
        Class to manipulate LZWOLFTEAM Compression

        Games where this compression is found:
            - [SMD] Earnest Evans
            - [SMD] Final Zone
            - [SMD] Granada
            - [SMD] El Viento
            - [SMD] Ranger-X
            - [SMD] Zan Yasha Enbuden.
    """

    def __init__(self, input_data):
        super(LZNEXTECH, self).__init__(input_data)


class LZANCIENT(LZSS):
    """
        Class to manipulate LZANCIENT Compression

        Games where this compression is found:
            - [SMD] Beyond Oasis
            - [SMD] Streets of Rage 2
    """

    signature = b'\x02\x00\x00\x60\xE7\x18\x06\x40\x00\x03\x02\x01\x00\x1F'

    def __init__(self, input_data):
        super(LZANCIENT, self).__init__(input_data)

    def bitclear(self, value=0x0, index=0):
        if (value >> index) & 0x1:
            return value ^ (1 << index)
        return value

    def rotate_bits_left(self, value=0x0, bits_to_rotate=0, max_bits=8):
        return (value << bits_to_rotate % max_bits) & (2**max_bits-1) | ((value & (2**max_bits-1)) >> (max_bits-(bits_to_rotate % max_bits)))

    def decompress(self, *args):
        offset = args[0]
        self._output = bytearray()
        self.DATA.ENDIAN = ">"
        self.DATA.set_offset(offset+2)
        if self.DATA.read_8() == 0x0:
            pass
        else:
            self.DATA.set_offset(offset)
            low, high = self.DATA.read_8(), self.DATA.read_8()
            # to little endian
            compressed_size = ((high << 8) | low)
            while (self.DATA.CURSOR < offset+compressed_size):
                ctrl = self.DATA.read_8()
                if not self.bitclear(ctrl, 7) == ctrl:
                    # LZ From buffer
                    ctrl = self.bitclear(ctrl, 7)
                    repeats = self.rotate_bits_left((ctrl & 0x60), 3) + 4
                    _readed = self.DATA.read_8()
                    position = ((ctrl & 0x1F) << 8) | _readed
                    for i in range(repeats):
                        self._output.append(
                            self._output[len(self._output)-position])

                    ctrl = self.DATA.read_8()
                    while True:
                        if (ctrl & 0xE0) == 0x60:
                            repeats = (ctrl & 0x1F)
                            for i in range(repeats):
                                self._output.append(
                                    self._output[len(self._output)-position])
                        else:
                            self.DATA.CURSOR -= 1
                            break
                        ctrl = self.DATA.read_8()
                elif not self.bitclear(ctrl, 6) == ctrl:
                    # RLE
                    ctrl = self.bitclear(ctrl, 6)
                    if self.bitclear(ctrl, 4) == ctrl:
                        repeats = ctrl + 4
                    else:
                        ctrl = self.bitclear(ctrl, 4)
                        repeats = ((ctrl << 8) | self.DATA.read_8()) + 4
                    _readed = self.DATA.read_8()
                    for i in range(repeats):
                        self._output.append(_readed)
                else:
                    # RAW
                    if self.bitclear(ctrl, 5) == ctrl:
                        length = ctrl
                    else:
                        ctrl = self.DATA.read_8()
                        length = ctrl
                    for i in range(length):
                        self._output.append(self.DATA.read_8())
        return self._output

    def compress(self):
        self.DATA.ENDIAN = '<'
        self._window = RingBuffer(0x2000, 0x00, 0x00)
        self._output = bytearray()
        self._output.append(0x0)
        self._output.append(0x0)
        self._encoded = 0
        self.LOOKAHEAD = 0b1111
        self.MIN_LENGTH = 4
        while self._encoded < self.DATA.SIZE:
            # Search for RLE match
            rle_match = self.find_best_rle_match()
            # Search for LZ matches
            lz_match = self.find_best_lz_match(llimit=False)
            # RAW
            if (rle_match < self.MIN_LENGTH) and (lz_match[1] < self.MIN_LENGTH):
                _readed = self.DATA.read_8()
                self._window.append(_readed)
                if self._window.CURSOR > 0x1FFF:
                    self.flush_raw()
                self._encoded += 1
            # RLE
            elif rle_match >= lz_match[1]:
                self.do_rle(rle_match)
            # LZ
            else:
                self.do_lz(lz_match)
        if self._window.CURSOR > 0:
            self.flush_raw()
        self._output[0] = len(self._output) & 0xFF
        self._output[1] = len(self._output) >> 8
        self._output.append(0x0)
        return self._output

    def do_rle(self, rle_match):
        if self._window.CURSOR > 0:
            self.flush_raw()
        for i in range(rle_match):
            _readed = self.DATA.read_8()
        self._encoded += rle_match
        rle_match -= self.MIN_LENGTH
        if rle_match > 0xF:
            self._output.append(0x40 | 0x10 | ((rle_match >> 8) & 0xF))
            self._output.append(rle_match & 0xFF)
        else:
            self._output.append(0x40 | (rle_match & 0xF))
        self._output.append(_readed)

    def do_lz(self, lz_match):
        if self._window.CURSOR > 0:
            self.flush_raw()
        self.DATA.CURSOR += lz_match[1]
        self._encoded += lz_match[1]
        lz_offset, lz_length = lz_match
        lz_length -= self.MIN_LENGTH
        length = 3 if lz_length > 3 else lz_length
        self._output.append(0x80 | (length << 5) |
                            ((lz_offset >> 8) & 0x1F))
        self._output.append(lz_offset & 0xFF)
        lz_length -= length
        while lz_length > 0:
            length = 0x1F if lz_length > 0x1F else lz_length
            self._output.append(0x60 | length)
            lz_length -= length

    def flush_raw(self):
        if self._window.CURSOR > 0x1F:
            self._output.append(0x20 | ((self._window.CURSOR >> 8) & 0x1F))
            self._output.append(self._window.CURSOR & 0xFF)
        else:
            self._output.append(self._window.CURSOR)
        for i in range(0, self._window.CURSOR):
            self._output.append(self._window._buffer[i])
        self._window.byte_fill(self._window.BYTE_FILL)
        self._window.CURSOR = 0


class RLESOFTWARECREATIONS(RLE):
    """
        Class to manipulate RLESOFTWARECREATIONS Compression

        Games where this compression is found:
            - [SMD] Cuthroat Island
            - [SMD] Spider Man and Venom: Separation Anxiety
            - [SMD] Spider Man and Vemom: Maximum Carnage
            - [SMD] The Tick
    """

    signature = b'\x10\x18\xB6\x00\x66\x16\x10\x18\x14\x18\x53\x02\x02'
    signature += b'\x42\x00\xFF\x4E\x92\x51\xCA\xFF\xFC\x57\x44\x66'

    def __init__(self, input_data):
        super(RLESOFTWARECREATIONS, self).__init__(input_data)

    def decompress(self, *args):
        offset = args[0]
        size = args[1]
        self.DATA.ENDIAN = '<'
        self._buffer = bytearray()
        self.DATA.set_offset(offset)
        temp = self.DATA.read_8()
        while size > 0:
            temp2 = self.DATA.read_8()
            if temp == temp2:
                value = self.DATA.read_8()
                length = self.DATA.read_8()
                for i in range(length):
                    self._buffer.append(value)
                size -= 3
            else:
                self._buffer.append(temp2)
                size -= 1
        return self._buffer

    def compress(self, *args):
        offset = args[0]
        self.DATA.ENDIAN = '<'
        self._output = bytearray()
        self._encoded = 0
        self.DATA.set_offset(offset)
        temp = self.DATA.read_8()
        self._output.append(temp)
        self.DATA.set_offset(offset)
        while self._encoded < self.DATA.SIZE:
            rle_match = self.find_best_rle_match()
            rle_match &= 0xFF
            if rle_match > 3:
                for i in range(rle_match):
                    _readed = self.DATA.read_8()
                self._output.append(temp)
                self._output.append(_readed)
                self._output.append(rle_match)
                self._encoded += rle_match
            else:
                self._output.append(self.DATA.read_8())
                self._encoded += 1
        return self._output

# class LZKOEI(LZSS):
#     def __init__(self):
#         pass


# class LZFACTOR5(LZSS):
#     def __init__(self):
#         pass


# class LZTECMO(LZSS):
#     def __init__(self):
#         pass

# class RLE_SNK(Compression):
#    def __init__(self):
#       pass


# class ITL(Compression):
#     # Variação da Altered
#     def __init__(self, input_data):
#         super(ITL, self).__init__(input_data)


class RNC(Compression):
    signature = b'\x52\x4E\x43'

    def __init__(self, input_data):
        super(RNC, self).__init__(input_data)

# class MUMMRA(LZSS):
#     def __init__(self, input_data):
#         super(MUMMRA, self).__init__(input_data)

#     def decompress(self, offset=0):
#         self.DATA.set_offset(offset)
#         self.DATA.ENDIAN = ">"
#         self._window = RingBuffer(0x400, 0x3DF)
#         self._buffer = bytearray()
#         terminate = False
#         _decoded = 0
#         while (self.DATA.CURSOR < self.DATA.SIZE) and (terminate == False):
#             control = 0xFF00 | self.DATA.read_8()
#             for readed_bits in range(8):
#                 bit = bool((control >> (7-readed_bits)) & 0x1)
#                 _readed = self.DATA.read_8()
#                 if bit:
#                     if _readed == 0x1F:
#                         terminate = True
#                     elif _readed < 0x80:
#                         length = (_readed & 0x1F) + 3
#                         offset = ((_readed & 0x60) << 3) | self.DATA.read_8()
#                         _decoded += self.append_from_window(length, offset)
#                     elif _readed >= 0x80 and _readed <= 0xC0:
#                         length = ((_readed >> 4) & 0x3) + 2
#                         offset = (self._window.CURSOR-(_readed & 0xF))
#                         _decoded += self.append_from_window(length, offset)
#                     else:
#                         length = (_readed & 0x3F) + 8
#                         _decoded += self.append_from_data(length)
#                 else:
#                     _decoded += self.append(_readed)
#         return self._buffer
