# echo-server.py

# from time import sleep
from multiprocessing.connection import wait
import socket

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 8080  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:

            data = conn.recv(1024)
            if data.decode() == "stop":
                print("Conexão encerrada.")
                break
            print(data.decode())
            while True:
              msg = input("Write your message: ")
              if msg == "stop":
                  conn.sendall(bytes("stop", encoding='utf-8'))
                  print("Conexão Encerrada")
                  conn.close()
                  break
              if msg != '': 
                  bitzada = bytes(msg, encoding='utf-8')
                  conn.sendall(bitzada)
                  break
              else:
                  print("msg nula, tente dnv")
                  