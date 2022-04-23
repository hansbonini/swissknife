from .base import *

name = "8BPP Linear"
description = "8 bits per pixel linear Codec"
version = "1.0"

class BPP8_Linear(BaseCodec):

    def __init__(self, *args):
        super().__init__(*args)

    def process(self):
        for i in range(0, self.eof):        
            temp = int.from_bytes(self.binary.file.read(1), byteorder='big')
            # Load 2 nibbles into Pixels
            self.pixels.append(temp)