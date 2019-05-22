from socket import*
import sys
import threading
import os
import time

user=list()
usuarios=list()
canales=list()
servidor_encendido = 1

def primer_login(socketServer):
    cliente,direccion = socketServer.accept()
    cliente.send("Introduce tu nombre de usuario: ")
    username = cliente.recv(2048)
    user.append(username)
    user.append(direccion)
    user.append(cliente)
    usuarios.append(user)
    x=threading.Thread(target=recibo,args=(cliente,))
    x.start()

def login(socketServer):
    servidor_encendido = 1
    while 1:
        cliente,direccion = socketServer.accept()
        cliente.send("Introduce tu nombre de usuario: ")
        username = cliente.recv(2048)
        while username in usuarios:
            print "Usuario ya en el sistema"
            cliente.send("Nombre no disponible.\nIntroduce tu nombre de usuario: ")
            username = cliente.recv(2048)
        user[0] = username
        user[1] = direccion
        user[2] = cliente
        cliente.send("Bienvenido al servidor!")
        print "Usuario %s ha entrado al sistema"
        usuarios.append(user)
        x=threading.Thread(target=recibo,args=(cliente,))
        x.start()

def ini_server():
    serverIp = ''
    serverPort = input('Introduce el puerto del servidor:')
    dataConection = (serverIp,serverPort)
    #creamos el socket de conexiones
    socketServer = socket(AF_INET,SOCK_STREAM)
    socketServer.bind(dataConection)

def envio(socketClient,mensaje):
    while servidor_encendido:
        socketClient.send(mensaje)

def recibo(cliente):
    print "Cliente" + str(cliente) + "esta a la escucha :)"
    while 1:
        respuesta=cliente.recv(2048)
        print(respuesta)
        if respuesta == "EXIT":
            servidor_encendido = 0

def main():
    serverIp = '127.0.0.1'
    serverPort = input('Introduce el puerto del servidor:')
    dataConection = (serverIp,serverPort)
    #creamos el socket de conexiones
    socketServer = socket(AF_INET,SOCK_STREAM)
    socketServer.bind(dataConection)
    socketServer.listen(100)
    primer_login(socketServer)
    x=threading.Thread(target=login,args=(socketServer,))
    x.start()

main()
