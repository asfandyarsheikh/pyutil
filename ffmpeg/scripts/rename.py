import os, glob

path = os.getcwd()
files = glob.glob(path + '/*.rar')
print(files)
for f in files:
    arr = f.split(".")
    modified = arr[-2]
    if (modified.find("part") >= 0 and modified.find("-") >= 0):
        newmod = modified.split("-")[0]
        arr[-2] = newmod
        finalname = ".".join(arr)
        os.rename(f, finalname)
