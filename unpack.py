#!/usr/bin/env python
#
# based on https://pastebin.com/raw/9w5TBnSv
# credits to original author HemanthJabalpuri @ XDA
# converted to python using chatgpt

import struct
import sys

def abort(msg):
    sys.stderr.write(msg + "\n")
    sys.exit()

def get_string(f, n):
    dat = f.read(n)
    return dat.replace(b"\x00", b"")

def get_long(f):
    long_bytes = f.read(8)
    long_value = struct.unpack("Q", long_bytes)[0]
    return long_value

def extract(name, offset, length):
    with open(name, "wb") as of:
        f.seek(offset)
        of.write(f.read(length))

if len(sys.argv) < 2:
    abort("Usage: unpack.py radio.img")

with open(sys.argv[1], "rb") as f:
    magic = get_string(f, 256)
    if magic != b"SINGLE_N_LONELY":
        abort("Unsupported")

    fsize = f.seek(0, 2)
    f.seek(256)

    for i in range(1, 65):
        name = get_string(f, 248)
        size = get_long(f)
        if name == b"LONELY_N_SINGLE":
            break  # no more files
        
        extract(name.decode(), f.tell(), size)
        pad = 0
        if size % 4096 != 0:
            pad = 4096 - (size % 4096)
            f.read(pad)
        print("Name: {}, Offset: {}, Size: {}, Padding: {}".format(name.decode(), f.tell(), size, pad))
