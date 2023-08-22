import ffmpeg, os, shutil, string
from ffutil import *
from varlist import *

def file_list():
    lst = list_mkv(temppath)
    with open(mp4_list, 'w') as f:
        for item in lst:
            f.write("file '%s'\n" % item)

def get_streams(input):
    istream = ffmpeg.input(input)
    streams = ffmpeg.probe(input)["streams"]
    output = []
    for stream in streams:
        if stream["codec_type"] == "video":
            output.append(istream.video)
        if stream["codec_type"] == "audio":
            output.append(istream.audio)
    return output

def process_encode(input, output):
    try:
        streams = get_streams(input)
        stream = ffmpeg.output(*streams, output, preset="veryfast", vcodec='libx264', crf=27, s="960x540", map="0:a?", strict="-2").overwrite_output()
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
    except ffmpeg._run.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
        pass

def encode(path, ix=0):
    lst = list_mp4(path)
    if (len(lst) is 0):
        lst = list_mkv(path, True)
    if (len(lst) is 0):
        lst = list_m4v(path)
    if (len(lst) is 0):
        lst = list_MP4(path)
    print(lst)
    print(len(lst))
    if (ix > 0):
        lst = lst[ix:]
    else:
        clear_dir(temppath)
    for idx, val in enumerate(lst):
        outpath = temppath + "/" + str(idx+ix) + ".mkv"
        process_encode(val, outpath)


def encode_cp(path, ix=0):
    lst = list_mp4(path)
    if (len(lst) is 0):
        lst = list_mkv(path, True)
    if (len(lst) is 0):
        lst = list_m4v(path)
    if (len(lst) is 0):
        lst = list_MP4(path)
    print(lst)
    print(len(lst))
    if (ix > 0):
        lst = lst[ix:]
    else:
        clear_dir(temppath)
    for idx, val in enumerate(lst):
        outpath = temppath + "/" + str(idx+ix) + ".mkv"
        shutil.copy(val, outpath)


valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

def sanitize(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tup = os.path.basename(path)
    s = "".join(x for x in tup if x in valid_chars)
    return os.path.join(os.path.dirname(path), s)

def encode_single(path):
    lst = list_files(path)
    lth = len(lst)
    for count, val in enumerate(lst):
        print(f"{count} of {lth}")
        if os.path.isdir(val):
            continue
        tup = os.path.splitext(val)
        if(tup[1] in (".mkv", ".m4v", ".mp4", ".MP4", ".ts")):
            outpath = tup[0].replace(inputpath, singlepath) + '.mp4'
            outpath = sanitize(outpath)
            process_encode(val, outpath)
            print(outpath)
        else:
            outpath = val.replace(inputpath, singlepath)
            outpath = sanitize(outpath)
            print(outpath)
            shutil.copy2(val, outpath)
    remove_dir(path)

def encode_del(path):
    lst = list_files(path)
    lth = len(lst)
    for count, val in enumerate(lst):
        print(f"{count} of {lth}")
        if os.path.isdir(val):
            continue
        tup = os.path.splitext(val)
        if(tup[1] in (".mkv", ".m4v", ".mp4", ".MP4", ".ts")):
            outpath = tup[0].replace(inputpath, singlepath) + '.mp4'
            outpath = sanitize(outpath)
            process_encode(val, outpath)
            os.remove(val)
            print(outpath)
        else:
            outpath = val.replace(inputpath, singlepath)
            outpath = sanitize(outpath)
            print(outpath)
            shutil.move(val, outpath, copy_function=shutil.copy2)
    remove_dir(path)

def combine(workdir):
    file_list()
    encodedfile = outputpath + "/" + final_mkv(workdir)
    stream = ffmpeg.input(mp4_list, format='concat', safe=0)
    stream = ffmpeg.output(stream, encodedfile, c='copy').overwrite_output()
    ffmpeg.run(stream)
    remove_dir(workdir)
    clear_dir(temppath)
