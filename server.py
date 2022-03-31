from asyncio.windows_events import NULL
import socket
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad


class SERVER:
    def __init__(self, host, port, passw):
        self.host = host
        self.port = port
        self.password = passw
        self.text = None
    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(6144)
                    data = self.descriptografar(self.password, data)
                    if data == "stop":
                        print("Conexão encerrada.")
                        break
                    print(data)
                    self.comunicar(conn)
    def comunicar(self, conn):
        while True:
            msg = input("Write your message: ")
            if msg == "stop":
                conn.sendall(self.criptografar(self.password, msg))
                print("Conexão Encerrada")
                conn.close()
                break
            if msg != '': 
                conn.sendall(self.criptografar(self.password, msg))
                break
            else:
                print("msg nula, tente dnv")
    def criptografar(self, senha, text):
        cipher = AES.new(senha.encode("utf-8"), AES.MODE_CBC)
        iv = cipher.iv
        textocodificado = iv + cipher.encrypt(pad(text.encode("utf-8"), AES.block_size))
        return textocodificado
    def descriptografar(self, senha, text):
        iv = text[:16]
        cipher = AES.new(senha.encode("utf-8"), AES.MODE_CBC, iv)
        textocodificado = text[16:]
        textocodificado = cipher.decrypt(textocodificado)
        textocodificado = unpad(textocodificado, AES.block_size)
        textocodificado = textocodificado.decode()
        return textocodificado
ip = input("Digite seu ip interno: ")
port = int(input("Digite a porta da conexão: "))
senha = input("Digite uma senha de 16 caracteres para a conexão (mesma do cliente): ")
conexao = SERVER(ip, port, senha)
conexao.connect()