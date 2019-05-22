from socket import*
import sys
import threading
import os


cliente_encendido = 1


def envio():
    while cliente_encendido:
        mensaje = raw_input('')
        socketClient.send(mensaje)

def recibo():
    while cliente_encendido:
        respuesta=socketClient.recv(2048)
        print(respuesta)


serverIp = raw_input('Introduce la direccion ip del servidor:')
serverPort = input('Introduce el puerto del servidor:')
dataConection = (serverIp,serverPort)
socketClient = socket(AF_INET,SOCK_STREAM)
socketClient.connect(dataConection)
x=threading.Thread(target=envio)
x.start()
x=threading.Thread(target=recibo)
x.start()
