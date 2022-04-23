import wave

class Audio:
    """
        Base class to manipulate Audio
    """

    def __init__(self, input_data):
        self._output = bytearray()
        self.DATA = input_data

    def to_wave(self, output_path, freq):
        wavefile = wave.open(output_path, 'wb')
        wavefile.setnchannels(1)
        wavefile.setsampwidth(1)
        wavefile.setframerate(freq)
        wavefile.writeframes(self._output)

class PCM(Audio):
    """
        Base class to manipulate Sega Genesis PCM
    """
    def __init__(self, input_data, offset, length):
        super(PCM, self).__init__(input_data)
        self.DATA.ENDIAN='>'
        self.DATA.set_offset(offset)
        while self.DATA.CURSOR < offset+length:
            pcm_data = self.DATA.read_8()          
            self.append_data(pcm_data)

    def append_data(self, data):
        self._output.append(data)

class DPCM(Audio):
    """
        Base class to manipulate Sega Genesis DPCM
    """

    delta = [
        0x0,
        0x1,
        0x2,
        0x4,
        0x8,
        0x10,
        0x20,
        0x40,
        -0x80,
        -0x1,
        -0x2,
        -0x4,
        -0x8,
        -0x10,
        -0x20,
        -0x40
    ]

    dpcm_start = 0x80

    def __init__(self, input_data, offset, length):
        super(DPCM, self).__init__(input_data)
        self.DATA.ENDIAN='>'
        self.DATA.set_offset(offset)
        pcm_data = self.dpcm_start
        while self.DATA.CURSOR < offset+length:
            dpcm_data = self.DATA.read_8()          
            pcm_data+=self.delta[(dpcm_data>>4)&0xF]
            self.append_data(pcm_data)
            pcm_data+=self.delta[dpcm_data&0xF]
            self.append_data(pcm_data)

    def append_data(self, data):
        print(data)
        if data >= 0:
            print(hex(data))
            self._output.append(data)
        else:
            signed = 0x100
            signed += data&0xFF
            signed &= 0xFF
            print(hex(signed))
            self._output.append(signed)



        
    

