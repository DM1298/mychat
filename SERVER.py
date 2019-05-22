from socket import*
import sys
import threading
import os
import time

usuarios=list()
canales=list()

def welcome(cliente):
    x="Bienvenido al servidor!\n Estos son los comandos que puedes realizar:"
    cliente.send(x)

def primer_login(socketServer):
    user=list()
    cliente,direccion = socketServer.accept()
    cliente.send("Introduce tu nombre de usuario: ")
    username = cliente.recv(2048)
    user.append(username)
    user.append(direccion)
    user.append(cliente)
    usuarios.append(user)
    nuevo_grupo=["GENERAL"]
    nuevo_grupo.append(user)
    canales.append(nuevo_grupo)
    x=threading.Thread(target=recibo,args=(cliente,username,direccion,))
    x.start()

def login(socketServer):
    user=list()
    while 1:
        cliente,direccion = socketServer.accept()
        cliente.send("Introduce tu nombre de usuario: ")
        username = cliente.recv(2048)
        if username == "EXIT":
            exit()
        while username in usuarios:
            print "Usuario ya en el sistema"
            cliente.send("Nombre no disponible.\nIntroduce tu nombre de usuario: ")
            username = cliente.recv(2048)
        user[0] = username
        user[1] = direccion
        user[2] = cliente
        cliente.send("Bienvenido al servidor!")
        print "Usuario " + userneme + " ha entrado al sistema"
        usuarios.append(user)
        x=threading.Thread(target=recibo,args=(cliente,username,direccion,))
        x.start()

def ini_server():
    serverIp = ''
    serverPort = input('Introduce el puerto del servidor:')
    dataConection = (serverIp,serverPort)
    #creamos el socket de conexiones
    socketServer = socket(AF_INET,SOCK_STREAM)
    socketServer.bind(dataConection)

def recibo(cliente,username,direccion,):
    canales_actuales["GENERAL"]
    user = list()
    user[0] = username
    user[1] = direccion
    user[2] = cliente
    while 1:
        respuesta=cliente.recv(2048)
        print(respuesta)
        if respuesta == "MOSTRA_CANALS":
            ver_canales(cliente)
        elif respuesta == "MOSTRA_USUARIS":
            ver_usuarios(cliente)
        elif respuesta == "MOSTRA_TOTS":
            ver_todos(cliente)
        elif respuesta[:6] == "PRIVAT":
            x="WORK IN PROGRESS...."
            envia(cliente,x)
        elif respuesta[:6] == "CANVIA":
            x="WORK IN PROGRESS...."
            envia(cliente,x)
            print respuesta[7:]
        elif respuesta[:4] == "CREA":
            crea_grupo(respuesta[5:],user)
            envia(cliente,"CANAL CREADO")
        elif respuesta == "EXIT":
            envia(cliente,"EXIT")
            #sal_del_sistema(user)
            print username + " se va!"
            exit()
        else:
            print "ENVIA MENSAJE AL GRUPO"


def envia(cliente,mensaj):
    mensaje = "SERVIDOR: " + str(mensaj)
    cliente.send(mensaje)

def crea_grupo(nuevo_grupo,user):
    nuevo_grupo.append(user)
    canales.append(nuevo_grupo)
    envia(user[2],"Gupo creado")

#FUncion para ver todos los usuarios del sistema
def ver_todos(socketClient):
    envia(socketClient,"SERVIDOR:")
    for x in range(len(usuarios)):
        socketClient.send(str(usuarios[x][0]))

#funcion para ver todos los canales del sistema
def ver_canales(socketClient):
    envia(socketClient,"SERVIDOR:")
    for x in range(len(canales)):
        socketClient.send(str(canales[x][0]))

#Funcion que borra al usuario del sistema
def sal_del_sistema(user):
    usuarios.remove(user[0])
    usuarios.remove(user[1])
    usuarios.remove(user[2])
    canales.remove(user[0])
    canales.remove(user[1])
    canales.remove(user[2])

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
    on = 1
    while on:
        command = raw_input("")
        if command == "EXIT":
            socketClient = socket(AF_INET,SOCK_STREAM)
            socketClient.connect(dataConection)
            socketClient.send("EXIT")
            on=0
            #for x in range(len(usuarios)):
            #    sal_del_sistema(usuarios[x])
    print "GOODBYE!"


main()
