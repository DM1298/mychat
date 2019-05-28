from socket import*
import sys
import threading
import os
import time

usuarios=list()
canales=list()
ocultos=list()

def welcome(cliente):
    x="Bienvenido al servidor!\n Estos son los comandos que puedes realizar:"
    cliente.send(x)
    ayuda(cliente)


def primer_login(socketServer):
    user=list()
    cliente,direccion = socketServer.accept()
    cliente.send("Introduce tu nombre de usuario: ")
    username = cliente.recv(2048)
    user.append(username)
    user.append(direccion)
    user.append(cliente)
    nuevo_grupo=["GENERAL"]
    nuevo_grupo.append(user)
    welcome(cliente)
    print "Usuario " + username + " ha entrado al sistema"
    usuarios.append(user)
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
        user.append(username)
        user.append(direccion)
        user.append(cliente)
        welcome(cliente)
        print "Usuario " + username + " ha entrado al sistema"
        usuarios.append(user)
        canales[0].append(user)
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
    canales_actuales = ["GENERAL"]
    canal_actual = "GENERAL"
    user = list()
    user.append(username)
    user.append(direccion)
    user.append(cliente)
    while 1:
        respuesta=cliente.recv(2048)
        print str(username) + ": " + respuesta
        if respuesta == "MOSTRA_CANALS":
            ver_canales(cliente)
        elif respuesta == "MOSTRA_USUARIS":
            ver_usuarios(cliente,canales_actuales)
        elif respuesta == "MOSTRA_TOTS":
            ver_todos(cliente)
        elif respuesta == "SURT_CANAL":
            canales_actuales.remove(canal_actual)
            surt_grup(user,canal_actual)
            canal_actual = ""
        elif respuesta[:6] == "PRIVAT":
            privado(username,respuesta[7:],cliente)
        elif respuesta[:6] == "CANVIA":
            canales_actuales.append(respuesta[7:])
            canal_actual = respuesta[7:]
            canvia_canal(user,respuesta[7:])
        elif respuesta[:4] == "CREA":
            crea_grupo(respuesta[5:],user)
            envia(cliente,"CANAL CREADO")
        elif respuesta[:11] == "CANAL_OCULT":
            crea_oculto(respuesta[12:],user)
            envia(cliente,"CANAL OCULTO CREADO")
        elif respuesta[:12] == "CANVIA_OCULT":
            canales_actuales.append(respuesta[13:])
            canvia_canal(user,respuesta[13:])
        elif respuesta == "HELP":
            ayuda(cliente)
        elif respuesta == "EXIT":
            envia(cliente,"EXIT")
            cliente.close()
            #sal_del_sistema(user)
            print username + " se va!"
            exit()
        else:
            for x in range(len(canales)):
                if canal_actual == canales[x][0]:
                    for z in range(len(canales[x])):
                        if z > 0:
                            canales[x][z][2].send(mensaje)
            #mensaje = username + ": " + respuesta
            #for x in range(len(canales)):
            #    for y in range(len(canales_actuales)):
            #        if canales[x][0] == canales_actuales[y]:
            #            for z in range(len(canales[x])):
            #                if z > 0:
            #                    canales[x][z][2].send(mensaje)
def ayuda(cliente):
    ayuda = open("help.txt","r")
    for mens in ayuda:
            cliente.send(mens)
    ayuda.close()

def surt_grup(user,canal):
    for x in range(len(canales)):
        if canales[x][0] == canal:
            canales[x].remove(user)
            user[2].send("Has salido del canal")

def envia(cliente,mensaj):
    mensaje = "SERVIDOR: " + str(mensaj)
    cliente.send(mensaje)

#Anade el usuario en el canal designado
def canvia_canal(user,canal):
    for x in range(len(canales)):
        if canales[x][0] == canal:
            canales[x].append(user)
            user[2].send("Canal anadido")

#Crea un nuevo canal en la lista de canales
def crea_grupo(nuevo_grupo,user):
    grupo = list()
    grupo.append(nuevo_grupo)
    grupo.append(user)
    canales.append(grupo)

#Crea un nuevo canal oculto en la lista de canales oclutos
def crea_oculto(nuevo_grupo,user):
    grupo = list()
    grupo.append(nuevo_grupo)
    grupo.append(user)
    ocultos.append(grupo)

#FUncion para ver todos los usuarios del sistema
def ver_todos(socketClient):
    for x in range(len(canales)):
        for z in range(len(canales[x])):
            if z == 0:
                socketClient.send(canales[x][z])
            else:
                socketClient.send(canales[x][z][0])


#funcion para ver todos los canales del sistema
def ver_canales(socketClient):
    for x in range(len(canales)):
        socketClient.send(str(canales[x][0]))

def privado(username,destino,cliente):
    for x in range(len(usuarios)):
        if str(destino) == str(usuarios[x][0]):
            cliente.send("Introduce el mensaje privado:")
            mensaje = cliente.recv(2048)
            mensaje = username + ": " + mensaje
            usuarios[x][2].send(mensaje)

def ver_usuarios(socketClient,canales_actuales):
    for x in range(len(canales)):
        for y in range(len(canales_actuales)):
            if canales[x][0] == canales_actuales[y]:
                for z in range(len(canales[x])):
                    if z == 0:
                        socketClient.send(canales[x][z])
                    else:
                        socketClient.send(canales[x][z][0])

#Funcion que borra al usuario del sistema
def sal_del_sistema(user):
    for x in range(len(usuarios)):
        usuarios[x].remove(user[0])
        usuarios[x].remove(user[1])
        usuarios[x].remove(user[2])
    for x in range(len(canales)):
        canales[x].remove(user[0])
        canales[x].remove(user[1])
        canales[x].remove(user[2])

def main():
    serverIp = ''
    serverPort = input('Introduce el puerto del servidor:')
    dataConection = (serverIp,serverPort)
    #creamos el socket de conexiones
    socketServer = socket(AF_INET,SOCK_STREAM)
    socketServer.bind(dataConection)
    socketServer.listen(1000)
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
        elif command == "CANALS_OCULTS":
            for x in range(len(ocultos)):
                print ocultos[x][0]
    print "GOODBYE!"


main()
