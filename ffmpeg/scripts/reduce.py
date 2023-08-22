from transcode import *
from ffutil import list_dir
from varlist import inputpath

def process():
    dirs = list_dir(inputpath)
    if (len(dirs) <= 0):
        print("FINISHED!!!!!")
        return    
    workdir = dirs[0]
    encode_single(workdir)
    process()

process()
