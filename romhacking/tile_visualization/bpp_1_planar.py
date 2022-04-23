from .base import *

name = "1BPP Planar"
description = "1 bit per pixel planar Codec"
version = "1.0"

class BPP1_Planar(BaseCodec):

    def __init__(self, *args):
        super().__init__(*args)

    def process(self):
        temp = self.to_planar()
        for i in range(0, len(temp)):
          # Load 8 bits into Pixels
            for bit in range(0,8):
                self.pixels.append((temp[i] >> bit)&0x1)