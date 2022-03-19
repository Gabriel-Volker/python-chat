# echo-client.py

import socket
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad

key = 'minhasenhaaaaaaa'
def criptografar(senha, text):
    cipher = AES.new(senha.encode("utf-8"), AES.MODE_CBC)
    iv = cipher.iv
    textocodificado = iv + cipher.encrypt(pad(bytes(text, encoding='utf8'), AES.block_size))
    return textocodificado

def descriptografar(senha, text):
    iv = text[:16]
    cipher = AES.new(senha.encode("utf-8"), AES.MODE_CBC, iv)
    textocodificado = text[16:]
    textocodificado = cipher.decrypt(textocodificado)
    textocodificado = unpad(textocodificado, AES.block_size)
    textocodificado = textocodificado.decode()
    return textocodificado
HOST = "192.168.1.178"  # The server's hostname or IP address
PORT = 8080  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        
        msg = input("Escreva uma Mensagem: ")
        if msg == "stop":
            print("Conexão Encerrada")
            s.sendall(criptografar(key, msg))
            break
        if msg != "":
          enviar = criptografar(key, msg)
          s.sendall(enviar)
          data = s.recv(6144)
          data = descriptografar(key, data)
          if data == "stop":
              print("Conexão Encerrada")
              break
          print("Resposta do Servidor: " + data)
        else:
          print("Mensgem nula, escreva novamente.")
          
 