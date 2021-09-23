#!/usr/bin/python
import mmap
from Crypto.Cipher import AES
from shutil import copyfile
import os
import sys
import re

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
        content = mm.read()
        aes_key = os.urandom(16)
        iv = os.urandom(16)
        #print(aes_key)
        #print(iv)
        aes = AES.new(aes_key, AES.MODE_CBC, iv)
        extra = len(content) % 16
        i = 0
        if extra > 0:
            content = content + (b'-' * (16 - extra))
        #print(16-extra)
        contentaes=aes.encrypt(content)
        #print(len(content))
        #print(contentaes)
        #print(len(contentaes))
        mm.flush()
        mm.close
        f.write(contentaes+b"AESKEYBEGIN"+aes_key+b"AESKEYEND"+iv+b"PADDINGBEGIN"+bytes(str(16-extra), "utf-8"))

def decrypt(file, outfile):
    with open(file, "r+b") as f:
        mm = mmap.mmap(f.fileno(),0)
        mm.seek(mm.find(b'PADDINGBEGIN',0))
        mm.seek(mm.tell()+12)
        paddinglen=int(mm.readline().decode("utf-8"))
        mm.seek(0)
        mm.seek(mm.find(b"AESKEYBEGIN"))
        currloc=mm.tell()
        #print(currloc)
        mm.seek(0)
        #currloc=mm.tell()
        #print(currloc)
        content=mm.read(currloc)
        #print(content)
        mm.seek(mm.find(b"AESKEYBEGIN",0))
        #print(mm.tell())
        mm.seek(mm.tell()+11)
        aes_key=(mm.read(16))
        #print(aes_key)
        #print(mm.find(b"AESKEYEND",0))
        mm.seek(mm.find(b"AESKEYEND",0))
        mm.seek(mm.tell()+9)
        iv=mm.read(16)
        #print(iv)
        contentstr=str(content)
        #print(contentstr)
        #print(len(content))
        aes = AES.new(aes_key, AES.MODE_CBC, iv)
        contentencr=aes.decrypt(content)
        #print(len(contentencr))
        mm.close
    with open(outfile, "wb") as f:
        f.write(contentencr)
    file = open(outfile).read()
    new_file = file[:-paddinglen]
    os.remove(outfile)
    open(outfile, 'w').write(new_file)



if len(sys.argv) <= 1:
    help()
elif len(sys.argv) <= 2:
    print("Please specify an input file!")
command = sys.argv[1]
if command in Decrypt:
    if len(sys.argv) == 3:
        if ".antinotechsavvy" in sys.argv[2]:
            outfile = sys.argv[2][:-11]
        else:
            outfile = sys.argv[2]+".decrypted"
    else:
        outfile = sys.argv[3]
    decrypt(sys.argv[2], outfile)
elif command in Encrypt:
    #print(command)
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
