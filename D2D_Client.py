import socket as sk
import pickle as pk
import sys

class Requisicaom2m:
    def __init__(self,readings, client_id):
        self.readings = readings
        self.client_id = str(client_id)

    def makeSignalMatrix(self):
        SigMat = dict()
        for r in self.readings: 
            SigMat[r.split(";")[0]] = r.split(";")[1:3]
        return SigMat

    def setReadings(self, readings):
        self.readings = readings

    def setClientId(self, client_id):
        self.client_id = client_id

    def getClientId(self):
        return self.client_id

readings = []
file_name = input("enter file name: ")
with open(file_name, "r") as file:
    text = file.readlines()
for i in range(0, len(text), 2):
    cont = ":".join(text[i].split(":")[1:]).strip()
    contx = text[i + 1].split("Quality=")[1]
    cont2 = contx.split("Signal level=")[0].strip()
    cont3 = contx.split("Signal level=")[1].strip()
    cont3 = cont3.split("dBm")[0].strip()
    readings.append(cont + ";" + cont3)


req = object.__new__(Requisicaom2m)

client_id = input("id do cliente:")

req.setClientId(client_id)
req.setReadings(readings)

tcpsk = sk.socket(sk.AF_INET, sk.SOCK_STREAM) #cria socket tcp
tcpsk.settimeout(10) #timout de 10 segundos
tcpsk.connect(("localhost", 8200)) #conecta o cliente com o servidor
                                               #no ip e portas esquecificados

while(True):
    try:
        message = pk.dumps(req) #transforma o objeto em cadeia de bytes
        tcpsk.send(message) #transmite os bytes do objeto
        data = tcpsk.recv(1024) #recebe o resultaado
        if(data != None):
            print("result:" + data.decode('utf8'))
            break
    except sk.timeout:
        print("timeout")
        break
tcpsk.close() #fecha o socket
