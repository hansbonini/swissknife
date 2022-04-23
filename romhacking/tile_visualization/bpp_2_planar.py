from .base import *

name = "2BPP Planar"
description = "2 bits per pixel planar Codec"
version = "1.0"

class BPP2_Planar(BaseCodec):

    def __init__(self, *args):
        super().__init__(*args)

    def process(self):
        temp = self.to_planar()
        for i in range(0, len(temp)):
            # Load 4 pairs of bits into Pixels
            self.pixels.append((temp[i] >> 6)&0x3)
            self.pixels.append((temp[i] >> 4)&0x3)
            self.pixels.append((temp[i] >> 2)&0x3)
            self.pixels.append((temp[i])&0x3)