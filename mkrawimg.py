#!/usr/bin/python3
from PIL import Image
import sys
from struct import pack

for arg in sys.argv[1:]:
    im = Image.open(arg)
    sz=im.size
    print(sz,arg)
    basename,ext=arg.split(".")
    newname=basename + ".raw"
    print("converting to raw:",newname)
    with open(newname,"wb") as of:
        of.write(pack(">LL",sz[0],sz[1]))
        for i in range(sz[0]):
            for j in range(sz[1]):
                r, g, b = im.getpixel((j,i))
                # convert to color565
                color=( (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3)
                of.write(pack(">H",color))