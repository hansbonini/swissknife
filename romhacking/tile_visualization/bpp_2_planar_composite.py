from .base import *

name = "2BPP Linear Composite (1bpp + 1bpp)"
description = "2 bits per pixel planar composite Codec"
version = "1.0"

class BPP2_Planar_Composite(BaseCodec):

    def __init__(self, *args):
        super().__init__(*args)

    def process(self):
        temp = self.to_composite()
        for i in range(0, len(temp)):
            # Load 4 pairs of bits into Pixels
            self.pixels.append((temp[i] >> 6)&0x3)
            self.pixels.append((temp[i] >> 4)&0x3)
            self.pixels.append((temp[i] >> 2)&0x3)
            self.pixels.append((temp[i])&0x3)