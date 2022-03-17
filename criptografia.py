from Cryptodome.Cipher import AES
from Crypto.Util.Padding import pad

key = bytes('minhasenhadesese', encoding='utf-8')
cipher = AES.new(key, AES.MODE_CBC)
texto = bytes("teste", encoding='utf-8')
textocodificado = cipher.encrypt(pad(texto, AES.block_size))
print(texto.decode())
print(textocodificado)
