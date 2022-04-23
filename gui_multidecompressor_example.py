import os
from os import SEEK_CUR, SEEK_END, SEEK_SET
from romhacking.common import ROM,TBL
from nes.data_compression import *
from utils.common import *
from gui.decompressor import MultiDecompressorWithTileViewerWindow

list_of_compressions = []


def decompress(rom_path, decompressed_data_path, codec=None, *args):
    print(rom_path)
    print(decompressed_data_pathLS -LAR)
    rom = ROM(rom_path, 'msb')
    algorithm = None
    for compression in FindAllSubclasses(Compression):
        if compression[1] == codec:
            algorithm = compression[0](rom)
    if algorithm:
        out = open(decompressed_data_path, 'wb')
        data = algorithm.decompress(*args)
        data_len = len(data)
        print('decompressed:{:08x}'.format(data_len))
        print('last: {:08x}'.format(rom.tell()))
        out.seek(0, 0)
        out.write(data)
        out.close()


def compress(rom_path, decompressed_data_path, codec=None, *args):
    offset = args[0]
    rom = open(rom_path, 'wb')
    input = ROM(decompressed_data_path, 'msb')
    algorithm = None
    for compression in FindAllSubclasses(Compression):
        if compression[1] == codec:
            algorithm = compression[0](input)
    if algorithm:
        data = algorithm.compress(offset)
        data_len = len(data)
        print('compressed:{:08x}'.format(data_len))
        rom.seek(offset, 0)
        rom.write(data)
        print('last: {:08x}'.format(rom.tell()))
        rom.close()
        input.close()


if __name__ == "__main__":
    
    for i in FindAllSubclasses(Compression):
       if i[1] == "LZSS" or i[1] == 'RLE':
           pass
       else:
           list_of_compressions.append(i[1])
    MultiDecompressorWithTileViewerWindow("Example NES MultiDecompressor with GUI", decompress, compress, codec_list=list_of_compressions)