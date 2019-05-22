from socket import*
import sys
import threading
import os


cliente_encendido = 1


def envio(socketClient):
    print cliente_encendido
    while cliente_encendido:
        mensaje = raw_input('Send: ')
        socketClient.send(mensaje)
        #if mensaje == "EXIT":
            #cliente_encendido = 0

def recibo(socketClient):
    while cliente_encendido:
        respuesta=socketClient.recv(2048)
        print(respuesta)
        #if respuesta == "EXIT":
            #cliente_encendido = 0


serverIp = raw_input('Introduce la direccion ip del servidor:')
serverPort = input('Introduce el puerto del servidor:')
dataConection = (serverIp,serverPort)
socketClient = socket(AF_INET,SOCK_STREAM)
socketClient.connect(dataConection)
x=threading.Thread(target=recibo,args=(socketClient,))
x.start()
x=threading.Thread(target=envio,args=(socketClient,))
x.start()
