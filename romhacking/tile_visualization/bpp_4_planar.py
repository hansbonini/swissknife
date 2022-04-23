from .base import *

name = "4BPP Planar"
description = "4 bits per pixel planar Codec"
version = "1.0"

class BPP4_Planar(BaseCodec):

    def __init__(self, *args):
        super().__init__(*args)

    def process(self):
        temp = self.to_planar()
        for i in range(0, len(temp)):
            # Load 2 nibbles into Pixels
            self.pixels.append((temp[i] >> 4)&0xF)
            self.pixels.append((temp[i])&0xF)