import socket as sk
import pickle as pk
import sys

class Requisicaom2m:
    def __init__(self,readings, client_id):
        self.readings = readings
        self.client_id = str(client_id)

    def makeSignalMatrix(self):
        file = open("tst.txt", "a")
        file.write(self.readings[:])

    def setReadings(self, readings):
        self.readings = readings

    def setClientId(self, client_id):
        self.client_id = client_id

    def getClientId(self):
        return self.client_id

readings = []
with open("tst.txt", "r") as file:
    text = file.readlines()
for i in range(1, len(text), 2):
    cont = ":".join(text[i - 1].split(":")[1:]).strip()
    cont2 = text[i].split(":")[1:]
    cont2[0] = cont2[0].split("Signal Level")[0].strip()
    cont2[1] = cont2[1].strip()
    readings.append(cont + ";" + cont2[0] + ";" + cont2[1])


req = object.__new__(Requisicaom2m)
req.setClientId("localhost")
req.setReadings(readings)

tcpsk = sk.socket(sk.AF_INET, sk.SOCK_STREAM) #cria socket tcp
tcpsk.settimeout(5) #timout de 5 segundos
tcpsk.connect(("localhost", 8000)) #conecta o cliente com o servidor
                                               #no ip e portas esquecificados

while(True):
    try:
        message = pk.dumps(req) #transforma o objeto em cadeia de bytes
        tcpsk.send(message) #transmite os bytes do objeto
        data = tcpsk.recv(1024) #recebe o resultaado
        if(data != ""):
            print("result:" + data.decode('utf8'))
            break
    except sk.timeout:
        print("timeout")
        break
tcpsk.close() #fecha o socket
