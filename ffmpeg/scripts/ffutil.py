import glob, os, re, shutil, ffmpeg
from pathlib import Path

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def list_mp4_nr(path):
    return natural_sort([file for file in glob.glob(path + "/*.mp4", recursive=False)])

def list_mp4(path, r=True):
    pathstr = "/**/*.mp4"
    if not r: pathstr = "/*.mp4"
    return natural_sort([file for file in glob.glob(path + pathstr, recursive=r)])

def list_MP4(path, r=True):
    pathstr = "/**/*.ts"
    if not r: pathstr = "/*.ts"
    return natural_sort([file for file in glob.glob(path + pathstr, recursive=r)])

def list_m4v(path, r=True):
    pathstr = "/**/*.m4v"
    if not r: pathstr = "/*.m4v"
    return natural_sort([file for file in glob.glob(path + pathstr, recursive=r)])

def list_mkv(path, r=False):
    pathstr = "/*.mkv"
    if r: pathstr = "/**/*.mkv"
    return natural_sort([file for file in glob.glob(path + pathstr, recursive=r)])

# def size_dir(path):
#    root_directory = Path(path)
#    x = [f.stat().st_size for f in root_directory.glob('**/*') if f.is_file() and f.suffix in (".mkv", ".m4v", ".mp4", ".MP4", ".ts")]
#    return sum(x) / len(x)

def size_dir(path):
    root_directory = Path(path)
    x = [(f.stat().st_size, f.resolve()) for f in root_directory.glob('**/*') if f.is_file() and f.suffix in (".mkv", ".m4v", ".mp4", ".MP4", ".ts")]
    y = sorted(x, key=lambda t: t[0], reverse=True)
    fil = y[0][1]
    w = ffmpeg.probe(fil, cmd='ffprobe')
    try:
        z = w['streams'][0]['bit_rate']
    except:
        z = w['streams'][1]['bit_rate']
    return int(z)

def list_dir(path):
    files = glob.glob(path + "/*/")
#    return sorted(files, key=lambda t: os.stat(t).st_mtime)
    return sorted(files, key=lambda t: size_dir(t), reverse=True)

def list_files(path):
    files = [os.path.join(root, name) for root, subdirs, files in os.walk(path) for name in files]
    print(path)
    print(files)
    files = [*set(files)]
    return sorted(files)

def clear_dir(path):
    files = glob.glob(path + '/*')
    for f in files:
        os.remove(f)

def remove_dir(path):
    shutil.rmtree(path)

def final_mkv(path):
    return path.split("/")[-2] + ".mkv"

def file_list(lst, mp4_list):
    with open(mp4_list, 'w') as f:
        for item in lst:
            f.write("file '%s'\n" % item)
    return lst
