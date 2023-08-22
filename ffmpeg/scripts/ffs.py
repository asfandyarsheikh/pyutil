from transcode import *
from ffutil import list_mp4_nr
from varlist import processpath

def process():
    dirs = list_mp4_nr(processpath)
    print(dirs)
    if (len(dirs) <= 0):
        print("FINISHED!!!!!")
        return
    encode_single(processpath)
    process()

process()
