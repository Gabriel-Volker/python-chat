# echo-client.py

import socket
from Cryptodome.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

class CLIENT:
    def __init__(self, host, port, senha):
        self.host = host
        self.port = port
        self.senha = senha
    def criptografar(self, senha, text):
        try:
            codigicacao = AES.new(senha.encode("utf-8"), AES.MODE_CBC)
            vetor_inicializacao = codigicacao.iv
            textocodificado = vetor_inicializacao + codigicacao.encrypt(pad(bytes(text, encoding='utf8'), AES.block_size))
            return textocodificado
        except:
            print("Houve um erro ao criptografar a mensagem.")
            exit()
    def descriptografar(self, senha, text):
        try:
            vetor_inicializacao = text[:16]
            codigicacao = AES.new(senha.encode("utf-8"), AES.MODE_CBC, vetor_inicializacao)
            textodecodificado = (unpad(codigicacao.decrypt(text[16:]), AES.block_size)).decode()
            return textodecodificado
        except:
            print("Houve um erro para decodificar a mensagem, você está utilizando a senha certa?")
            exit()
    def connect(self):
        try:
            key = self.senha
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                while True:
                    msg = input("Escreva uma Mensagem: ")
                    if msg == "stop":
                        print("Conexão Encerrada")
                        s.sendall(self.criptografar(key, msg))
                        break
                    if msg != "":
                        enviar = self.criptografar(key, msg)
                        s.sendall(enviar)
                        data = s.recv(6144)
                        data = self.descriptografar(key, data)
                        if data == "stop":
                            print("Conexão Encerrada")
                            break
                        print("Resposta do Servidor: " + data)
                    else:
                        print("Mensgem nula, escreva novamente.")
        except:
            print("Houve um erro na conexão com o servidor, revise os dados e tente novamente.")




HOST = input("Digite o ip do servidor: ")  # The server's hostname or IP address
PORT = int(input("Digite a porta da conexão: "))  # The port used by the server
key = input("Digite a senha de 16 caracteres para a conexão: ")
conectar = CLIENT(HOST, PORT, key)
conectar.connect()

          
 