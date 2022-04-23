from romhacking.common import ROM as GenericROM


class ROM(GenericROM):
    """
        Class to manipulate Sega Master System / Mark III
        ROM files
    """

    def __init__(self, filename, endian=None):
        super(ROM, self).__init__(filename, endian)
