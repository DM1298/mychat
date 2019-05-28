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
            exit()

def recibo(socketClient):
    prev_respuesta = ""
    while 1:
        respuesta=socketClient.recv(2048)
        if(prev_respuesta != respuesta):
            prev_respuesta=respuesta
            print(respuesta)
            if respuesta == "EXIT":
                socketClient.close()
                exit()



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
