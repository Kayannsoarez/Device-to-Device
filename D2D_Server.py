import socket as sk
import math as m
import threading as th
import multiprocessing as mp
import pickle as pk
import sys
#sfrom dicttoxml import dicttoxml

class Requisicaom2m:
    def __init__(self,readings, client_id):
        self.readings = readings
        self.client_id = str(client_id)

    def makeSignalMatrix(self):
        SigMat = dict()
        for r in self.readings: 
            SigMat[r.split(";")[0]] = r.split(";")[1]
        return SigMat
        
    def setReadings(self, readings):
        self.readings = readings

    def setClientId(self, client_id):
        self.client_id = client_id

    def getClientId(self):
        return self.client_id

#---------------------------------------------------------//////-------------------------
#Aqui começa o código do Servidor

limit = 2*mp.cpu_count() #Numero maximo de solicitacoes simultaneas permitido
started = [] #Vetor de threads vivas.
gdict = dict()
threshold = 0.8

def dictConstruct(consk, requisition):
    #@consk: socket criado pelo servidor para interagir com o cliente
    global gdict
    info = requisition.makeSignalMatrix()
    gdict[req.getClientId()] = info #atualiza o dicionário global com as informações do cliente

def dictProc(client_id):
    global gdict
    neighbor = [] #dicionario de correlacoes
    inner = 0
    norm1 = 0
    norm2 = 0
    tempdict = gdict
    power_vector = tempdict[client_id]

    for k in tempdict.keys():
        if(k != client_id):
            vector = tempdict[k]
            common = [key for key in vector if key in power_vector]
            if (len(common) > 0):
                for c in common:
                    inner = inner + float(vector[c])*float(power_vector[c])
                    norm1 = norm1 + float(vector[c])**2
                    norm2 = norm2 + float(power_vector[c])**2
                norm1 = m.sqrt(norm1)
                norm2 = m.sqrt(norm2)
                corr = inner/(norm1*norm2)
                if(corr >= threshold):
                    neighbor.append(k)
                else:
                    return "no neighbors"
            else:
                return "no neighbors"
    return neighbor


if(len(sys.argv) < 2):
    print("port has not been specified")
else:
    if(len(sys.argv) > 2):
        print("too much arguments. only the first will be used")
    tcp_server = sk.socket(sk.AF_INET, sk.SOCK_STREAM) #socket é criado
    tcp_server.bind(('', int(sys.argv[1]))) #Atrela o ip do servidor à porta especificada
    tcp_server.listen(limit) #Espera conexões e ouve no máximo limit conexões
    while(True):
        connectionsk, clientaddr = tcp_server.accept() #Forma conexão
        req = connectionsk.recv(1024)
        req = pk.loads(req) #transforma os bytes recebidos em um objeto
        solicitation = th.Thread(target = dictConstruct, args =\
                                 (connectionsk, req)) #Cria thread para
                                                             #conexão
        #Gerenciamento de concorrência
        if(len(started) <= limit): #imposição da eurística
            solicitation.start() #Inicia a thread
            started.append(solicitation) #Coloca a thread num vetor de threads ativas
        else:
            select = started[0]
            del started[0]
            select.join() #executa todas as threads até que select termine
        message = dictProc(req.getClientId())
        connectionsk.send(str(message).encode('utf8'))
connectionsk.close()
