# echo-client.py

import socket

HOST = "localhost"  # The server's hostname or IP address
PORT = 8080  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        
        msg = input("Escreva uma Mensagem: ")
        if msg == "stop":
            print("Conexão Encerrada")
            s.sendall(bytes(msg, encoding='utf-8'))
            break
        if msg != "":
          bitz = bytes(msg, encoding='utf-8')
          s.sendall(bitz)
          data = s.recv(1024)
          if data.decode() == "stop":
              print("Conexão Encerrada")
              break
          print("Resposta do Servidor: " + data.decode())
        else:
          print("Mensgem nula, escreva novamente.")
          
 