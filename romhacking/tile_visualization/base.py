from PIL import Image

class BaseCodec(object):
    def __init__(self, binary, palette=[], offset=0x0, w=16, h=16):
        self.buffer = Image.new('RGBA', (w*8, h*8), (0, 0, 0, 255))
        self.pixel_buffer = self.buffer.load()
        self.binary = binary
        self.palette = palette
        self.pixels = []
        self.offset = offset
        self.eof = offset+((w*8)*(h*8))+1
        self.binary.seek(offset,0)
        self.process()
        self.draw(w,h)
    
    def process(self):
        pass

    def to_planar(self):
        temp = []
        for i in range(0, self.eof//2):
            b1 = "{:08b}".format(int.from_bytes(self.binary.read(1), byteorder='big'))
            b2 = "{:08b}".format(int.from_bytes(self.binary.read(1), byteorder='big'))
            b3 = ""
            for i in range(len(b1)):
                b3+=(b2[i])
                b3+=(b1[i])
            temp.append(int(b3,2) >> 8)
            temp.append(int(b3,2) &0xFF)
        return temp

    def to_composite(self):
        temp1 = []
        temp2 = []
        temp3 = []
        for i in range(0, self.eof//8):
            for j in range(0,8):
                temp = int.from_bytes(self.binary.read(1), byteorder='big')
                if not i&1:        
                    temp1.append(temp)
                else:
                    temp2.append(temp)
        for i in range(0, self.eof//2):
            b1 = "{:08b}".format(temp1[i])
            b2 = "{:08b}".format(temp2[i])
            b3 = ""
            for i in range(len(b1)):
                b3+=(b2[i])
                b3+=(b1[i])
            temp3.append(int(b3,2) >> 8)
            temp3.append(int(b3,2) &0xFF)
        return temp3

    def draw(self, w, h):
        for i in range(0, len(self.pixels)):
            try:
                # Each tile column is result of modulo 8
                pixel_column = int(i % 8)
                # Each tile line is result of division by 8 then modulo 8
                pixel_line = int((i // 8) % 8)
                # Each tile is result of division by 64 = 8 columns * 8 lines
                tile = int(i // 64)
                # Each pixel bit is 1 color (multiply by 100 to convert to RGB)

                # Get X , Y and put on Image
                x = pixel_column + (tile * 8) % self.buffer.size[0]
                y = pixel_line + ((tile * 8) // self.buffer.size[1]) * 8

                # Draw Pixels on Pixel Buffer
                self.pixel_buffer[x, y] = self.palette[self.pixels[i]]
            except:
                pass

    def get_buffer(self):
        return self.buffer

    def get_pixel_buffer(self):
        return self.pixel_buffer