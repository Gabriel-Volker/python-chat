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
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print(f"Conectado em: {addr}")
                    while True:
                        data = conn.recv(6144)
                        data = self.descriptografar(self.password, data)
                        if data == False:
                            break
                        elif data == "stop":
                            print("Conexão encerrada.")
                            break
                        print(data)
                        manter_conexao = self.comunicar(conn)
                        if manter_conexao == False:
                            break
        except:
            print('Houve um erro na conexão')
    def comunicar(self, conn):
        while True:
            msg = input("Escreva sua mensagem: ")
            if msg == "stop":
                conn.sendall(self.criptografar(self.password, msg))
                print("Conexão Encerrada")
                conn.close()
                return False
                break
            if msg != '': 
                cripto = self.criptografar(self.password, msg)
                if cripto == False:
                    conn.close()
                    return False
                    break                  
                conn.sendall(self.criptografar(self.password, msg))
                break
            else:
                print("Mensagem nula, tente novamente.")
    def criptografar(self, senha, text):
        try:
            codificacao = AES.new(senha.encode("utf-8"), AES.MODE_CBC)
            vetor_inicializacao = codificacao.iv
            textocodificado = vetor_inicializacao + codificacao.encrypt(pad(text.encode("utf-8"), AES.block_size))
            return textocodificado
        except:
            print("Houve um erro em criptografar a mensagem.")
            return False
    def descriptografar(self, senha, text):
        try:
            vetor_inicializacao = text[:16]
            codificacao = AES.new(senha.encode("utf-8"), AES.MODE_CBC, vetor_inicializacao)
            textodecodificado = (unpad(codificacao.decrypt(text[16:]), AES.block_size)).decode()
            return textodecodificado
        except:
            print("Houve um erro na codificação da mensagem do cliente, provavelmente as senhas não coincidem")
            return False
ip = input("Digite seu ip interno: ")
port = int(input("Digite a porta da conexão: "))
senha = input("Digite uma senha de 16 caracteres para a conexão (mesma do cliente): ")
conexao = SERVER(ip, port, senha)
while True:
    conexao.connect()
    resposta = input("Deseja continuar escutando neste ip e porta? s/n: ")
    if resposta == "s":
        pass
    else:
        exit()
    print("Escutando novamente:")