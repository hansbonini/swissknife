from .base import *

name = "4BPP Planar Composite (2bpp x 2bpp)"
description = "4 bits per pixel planar composie Codec"
version = "1.0"

class BPP4_Planar_Composite(BaseCodec):

    def __init__(self, *args):
        super().__init__(*args)

    def process(self):
        temp = self.to_composite()
        for i in range(0, len(temp)):
            # Load 2 nibbles into Pixels
            self.pixels.append((temp[i] >> 4)&0xF)
            self.pixels.append((temp[i])&0xF)