from socket import*
import sys
import threading
import os


cliente_encendido = 1


def envio(socketClient):
    while 1:
        mensaje = raw_input('')
        socketClient.send(mensaje)
        if mensaje == "EXIT":
            threading.exit()

def recibo(socketClient):
    while 1:
        respuesta=socketClient.recv(2048)
        print(respuesta)
        if respuesta == "EXIT":
            socketClient.close()
            threading.exit()



serverIp = raw_input('Introduce la direccion ip del servidor:')
#serverIp = "0.0.0.0"
serverPort = input('Introduce el puerto del servidor:')
dataConection = (serverIp,serverPort)
socketClient = socket(AF_INET,SOCK_STREAM)
socketClient.connect(dataConection)
x=threading.Thread(target=recibo,args=(socketClient,))
x.start()
x=threading.Thread(target=envio,args=(socketClient,))
x.start()
