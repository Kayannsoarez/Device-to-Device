import socket as sk
import threading as th
import multiprocessing as mp
import pickle as pk
import sys

class Requisicaom2m:
    def __init__(self,readings, client_id):
        self.readings = readings
        self.client_id = str(client_id)

    def makeSignalMatrix(self):
        print(self.client_id + ":" + str(self.readings))
        return "Readings info received"


    def setReadings(self, readings):
        self.readings = readings

    def setClientId(self, client_id):
        self.client_id = client_id

    def getClientId(self):
        return self.client_id

limit = 2*mp.cpu_count()
started = [] #Vetor de threads vivas.

def connection(consk, clientaddr):
    #@consk: socket criado pelo servidor para interagir com o cliente
    #@clientaddr: tupla com o ip e a porta do cliente
    lock = th.Lock() #trava para a região crítica
    print("communication:{}".format(clientaddr))
    req = consk.recv(1024)
    req = pk.loads(req) #transforma os bytes recebidos em um objeto
    
    with lock:
        #Região crítica: escrita do arquivo compartilhado entre as threads
        result = req.makeSignalMatrix()
    #    requisitions = open('log.txt', 'a') #adiciona novas informações no final do arquivo
    #    requisitions.write("{}".format(clientaddr) + ":" + "{}".format(result))
    #    requisitions.close()        
    consk.send(result.encode('utf8')) #Envia o resultado ao cliente
    consk.close() #encerra o socket


    

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
        solicitation = th.Thread(target = connection, args =\
                                 (connectionsk, clientaddr)) #Cria thread para
                                                             #conexão
        #Gerenciamento de concorrência
        if(len(started) <= limit): #imposição da eurística
            solicitation.start() #Inicia a thread
            started.append(solicitation) #Coloca a thread num vetor de threads ativas
        else:
            select = started[0]
            del started[0]
            select.join() #executa todas as threads até que select termine
