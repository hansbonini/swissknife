from romhacking.common import ROM as GenericROM


class ROM(GenericROM):
    """
        Class to manipulate Sega Genesis / Mega Drive
        ROM files
    """

    def __init__(self, filename, endian=None):
        super(ROM, self).__init__(filename, endian)

    def get_system_type(self):
        self.set_offset(0x100)
        return self.read_ascii_str(16)

    def get_copyright(self):
        self.set_offset(0x110)
        return self.read_ascii_str(16)

    def get_title(self):
        region = self.get_region()
        self.set_offset(0x120)
        if region[0] == 'J':
            return self.read_sjis_str(48)
        else:
            return self.read_ascii_str(48)

    def get_international_title(self):
        region = self.get_region()
        self.set_offset(0x150)
        if region[0] == 'J':
            return self.read_sjis_str(48)
        else:
            return self.read_ascii_str(48)

    def get_serial_number(self):
        self.set_offset(0x180)
        return self.read_ascii_str(14)

    def get_checksum(self):
        self.set_offset(0x18E)
        return self.read_ascii_str(2)

    def get_region(self):
        self.set_offset(0x1F0)
        return list(self.read_ascii_str(3))

    def read_pointer_abs(self):
        return self.read_32()

    def read_pointer_rel(self):
        return self.read_16()
