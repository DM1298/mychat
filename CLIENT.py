from socket import*
import sys
import threading
import os

#FUncion que envia mensajes al socket pasado por parametro
def envio(socketClient):
    while 1:
        mensaje = raw_input('')
        socketClient.send(mensaje)
        if mensaje == "EXIT":
            exit()
#FUncion que esta a la espera de la recepcion de mensajes por parte del servidor
#SI el servidor le envia un EXIT, el cliente cierra la conexion con el servidor
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


#Se le pide al usuario la direccion IP/URL del servidor, asi como el puerto por el cual corre el servicio del chat
serverIp = raw_input('Introduce la direccion ip del servidor:')
#serverIp = "0.0.0.0"
serverPort = input('Introduce el puerto del servidor:')
dataConection = (serverIp,serverPort)
socketClient = socket(AF_INET,SOCK_STREAM)
socketClient.connect(dataConection)
#Crea dos threads, uno dedicado al envio de invormacion y el otro dedicado a la recepcion de la misma
x=threading.Thread(target=recibo,args=(socketClient,))
x.start()
x=threading.Thread(target=envio,args=(socketClient,))
x.start()
