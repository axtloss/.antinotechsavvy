#!/usr/bin/python
import mmap
from Crypto.Cipher import AES
from shutil import copyfile
import os
import sys

Decrypt = ["decrypt","-d"]
Encrypt = ["encrypt","-e"]
giveHelp = ["help","-h"]



def help():
    print(
        """usage: antinotech <option> <inputfile> [outputfile]
        \u2666 decrypt -d   -   decrypt a file to make it readable
        \u2666 encrypt -e   -   encrypt a file to make it not readable
        """
    )

def encrypt(file, outfile):
    copyfile(file, outfile)
    with open(outfile, "r+b") as f:
        mm = mmap.mmap(f.fileno(),0)
        content = mm.readline()
        aes_key = os.urandom(16)
        iv = os.urandom(16)
        print(aes_key)
        print(iv)
        aes = AES.new(aes_key, AES.MODE_CBC, iv)
        extra = len(content) % 16
        if extra > 0:
            content = content + (b'-' * (16 - extra))
        contentaes=aes.encrypt(content)
        print(content)
        print(contentaes)
        mm.flush()
        mm.close
        f.write(contentaes+b"aes"+aes_key+b"AES"+iv)

def decrypt(file, outfile):
    with open(file, "r+b") as f:
        mm = mmap.mmap(f.fileno(),0)
        mm.seek(mm.find(b"aes"))
        currloc=mm.tell()
        print(currloc)
        mm.seek(0)
        #currloc=mm.tell()
        print(currloc)
        content=mm.read(currloc)
        print(content)
        mm.seek(mm.find(b"aes",0))
        print(mm.tell())
        mm.seek(mm.tell()+3)
        aes_key=(mm.read(16))
        print(aes_key)
        print(mm.find(b"AES",0))
        mm.seek(mm.find(b"AES",0))
        mm.seek(mm.tell()+3)
        iv=mm.read(16)
        print(iv)
        contentstr=str(content)
        print(contentstr)
        print(len(content))
        aes = AES.new(aes_key, AES.MODE_CBC, iv)
        contentencr=aes.decrypt(content)
        mm.close
    with open(outfile, "wb") as f:
        output=contentencr.decode("utf-8")
        output=output.strip("-")
        f.write(bytes(output,"utf-8"))

if len(sys.argv) <= 1:
    help()
elif len(sys.argv) <= 2:
    print("Please specify an input file!")
command = sys.argv[1]
if command in Decrypt:
    if len(sys.argv) == 3:
        outfile = sys.argv[2].strip(".antinotech")
    else:
        outfile = sys.argv[3]
    decrypt(sys.argv[2], outfile)
elif command in Encrypt:
    print(command)
    if len(sys.argv) == 3:
        outfile = sys.argv[2]+".antinotech"
    else:
        outfile = sys.argv[3]
    print(sys.argv[2])
    print(outfile)
    encrypt(sys.argv[2],outfile)
elif command in giveHelp:
    help()
else:
    help()