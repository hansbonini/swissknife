from .base import *

name = "2BPP Linear"
description = "2 bits per pixel linear Codec"
version = "1.0"

class BPP2_Linear(BaseCodec):
    
    def __init__(self, *args):
        super().__init__(*args)

    def process(self):
        for i in range(0, self.eof):        
            temp = int.from_bytes(self.binary.file.read(1), byteorder='big')
            # Load 4 pairs of bits into Pixels
            self.pixels.append((temp >> 6)&0x3)
            self.pixels.append((temp >> 4)&0x3)
            self.pixels.append((temp >> 2)&0x3)
            self.pixels.append((temp)&0x3)