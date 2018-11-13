#Programa : Teste porta Raspberry Pi e Linux
#Autor : Kayann
 
#define o tempo que o led ficara aceso ou apagado
tempo = 2
 
#Define biblioteca da GPIO
import RPi.GPIO as GPIO
 
#Define biblioteca de tempo
import time                           
GPIO.setmode(GPIO.BOARD)
 
#Define o pino 12 da placa como saida
GPIO.setup(12, GPIO.OUT)
 
#rotina para acender o led
def acendeled(pino_led):
    GPIO.output(pino_led, 1)
    return
 
#rotina para apagar o led
def apagaled(pino_led):
    GPIO.output(pino_led, 0)
    return

#Inicia loop
while(1):
    #Simula O nÓ de devices pra acender o Led
    no = int(input())
    if(no == 2):
        #Acende o led
        acendeled(12)
        #Aguarda  segundo
        time.sleep(tempo)
        #apaga o led
        apagaled(12)
        #Aguarda meio segundo e reinicia o processo
        time.sleep(tempo)
    else:
        break;
        
        
    

