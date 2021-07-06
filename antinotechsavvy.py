import string
import random
import mmap
from Crypto.Cipher import AES
from shutil import copyfile
import os
import re


with open("hello.txt", "wb") as f:
    f.write(b"Hello World!\n")

copyfile("hello.txt", "hello.txt.antinotech")

def encrypt():
    with open("hello.txt.antinotech", "r+b") as f:
        mm = mmap.mmap(f.fileno(),0)
        content = mm.readline()
        aes_key = os.urandom(16)
        iv = os.urandom(16)

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

def decrypt():
    with open("hello.txt.antinotech", "r+b") as f:
        mm = mmap.mmap(f.fileno(),0)
        mm.seek(mm.find(b"aes"))
        currloc=mm.tell()
        print(currloc)
        mm.seek(0)
        print(currloc)
        content=mm.read(currloc)
        print(content)
        mm.find(b"aes")
        mm.seek(mm.tell()+4)
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
        print(contentencr)
        mm.close
        print(content.decode("utf-8"))
#decrypt()
encrypt()
