from .base import *

name = "1BPP Linear"
description = "1 bit per pixel linear Codec"
version = "1.0"

class BPP1_Linear(BaseCodec):
    
    def __init__(self, *args):
        super().__init__(*args)

    def process(self):
        for i in range(0, self.eof):        
            temp = int.from_bytes(self.binary.file.read(1), byteorder='big')
            # Load 8 bits into Pixels
            for bit in range(0,8):
                self.pixels.append((temp >> bit)&0x1)