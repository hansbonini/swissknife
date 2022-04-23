from .base import *

name = "4BPP Linear"
description = "4 bits per pixel linear Codec"
version = "1.0"

class BPP4_Linear(BaseCodec):

    def __init__(self, *args):
        super().__init__(*args)

    def process(self):
        for i in range(0, self.eof):        
            temp = int.from_bytes(self.binary.read(1), byteorder='big')
            # Load 2 nibbles into Pixels
            self.pixels.append((temp >> 4)&0xF)
            self.pixels.append((temp)&0xF)