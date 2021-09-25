# Antinotechsavvy

Encrypt your files to make it unreadable for not tech savvy people

# Important note
Do not use this to secure important data, the way this works is very simple and can be decoded very fast

# How does it work
It first reads the binary contents of the specified file <br>
then it generates a random aes key and aes iv <br>
it encrypts the contents of the file using those generated keys <br>
then it writes the encrypted content in a new file <br>
adds a "stop" called "aes", after which the aes key gets written <br>
and then another "stop" called "AES", after which the iv gets written <br>
<br>
this allows everyone with this program to decode the file, since the key is integrated in the file <br>
hope you see now why I added that important note

# How to use it
you only need to run the antinotechsavvy.py file!
to decrypt the file you use
```
python antinotechsavvy -d path/to/encrypted.antinotech path/to/output
```
to encrypt the file you use
```
python antinotechsavvy -e path/to/file-to-encrypt path/to/output.antinotech
```
the last output flag is not needed
using `decrypt` instead of `-d` or `encrypt` instead of `-e` works too

