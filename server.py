# echo-server.py

import socket
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad

HOST = "192.168.1.178"  # Standard loopback interface address (localhost)
PORT = 8080  # Port to listen on (non-privileged ports are > 1023)

key = 'minhasenhaaaaaaa'
def criptografar(senha, text):
    cipher = AES.new(senha.encode("utf-8"), AES.MODE_CBC)
    iv = cipher.iv
    textocodificado = iv + cipher.encrypt(pad(text.encode("utf-8"), AES.block_size))
    return textocodificado

def descriptografar(senha, text):
    iv = text[:16]
    cipher = AES.new(senha.encode("utf-8"), AES.MODE_CBC, iv)
    textocodificado = text[16:]
    textocodificado = cipher.decrypt(textocodificado)
    textocodificado = unpad(textocodificado, AES.block_size)
    textocodificado = textocodificado.decode()
    return textocodificado

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:

            data = conn.recv(6144)
            data = descriptografar(key, data)
            if data == "stop":
                print("Conexão encerrada.")
                break
            print(data)
            while True:
              msg = input("Write your message: ")
              if msg == "stop":
                  conn.sendall(criptografar(key, msg))
                  print("Conexão Encerrada")
                  conn.close()
                  break
              if msg != '': 
                  conn.sendall(criptografar(key, msg))
                  break
              else:
                  print("msg nula, tente dnv")
                  