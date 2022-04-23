import os
from os import SEEK_CUR, SEEK_END, SEEK_SET
from romhacking.common import ROM
from nes.data_compression import *
from utils.common import *


if __name__ == "__main__":

    path = '/home/hansb/Romhacking/nes_goemon2'
    list_of_files = []
    list_of_compressions = FindAllSubclasses(Compression)
    for root, dirs, files in os.walk(path):
       for file in files:
           list_of_files.append(os.path.join(root, file))
    for name in list_of_files:
       print('{}'.format(20*'-'))
       rom = ROM(name, 'big')
       print(name.replace(path, ''))
       for i in list_of_compressions:
           codec = i[0](rom)
           if codec.signature != None:
               buf = rom.read()
               if rom.search_bytes(codec.signature):
                   print('\t - Possible {} found!'.format(i[1]))
       rom.close()