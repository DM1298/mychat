from socket import*
import sys
import threading
import os
import time

usuarios=list()
canales=list()
ocultos=list()

#Pantalla debienvenida para cada cliente, muestra los comando disponobles y una pequena descripcion de los mismos.
def welcome(cliente):
    x="Bienvenido al servidor!\n Estos son los comandos que puedes realizar:"
    cliente.send(x)
    ayuda(cliente)

#Funcion para el primer usuario conectado, acepta la conexion entrante, le pide un nombre de usuario,
#anade el grupo GENERAL a la lista de grupos y mete al usuario dentro de la lista de usuarios y anade
# al usuario al grupo general dentro de la lista de canales.
#Al final inicia un nuevo thread por cada cliente.
def primer_login(socketServer):
    user=list()
    cliente,direccion = socketServer.accept()
    cliente.send("Introduce tu nombre de usuario: ")
    username = cliente.recv(2048)
    user.append(username)
    user.append(direccion)
    user.append(cliente)
    nuevo_grupo=["GENERAL"]
    welcome(cliente)
    print "Primer usuario " + username + " ha entrado al sistema"
    usuarios.append(user)
    canales.append(nuevo_grupo)
    canales[0].append(user)
    x=threading.Thread(target=recibo,args=(cliente,username,direccion,))
    x.start()

#Funcion las conexiones entrantes que no sean la primera, acepta la conexion entrante, le pide un nombre de usuario,
# en caso de que el nombre de usuario ya este en el sistema le pedira un segundo nombre de usuario al cliente
#y mete al usuario dentro de la lista de usuarios y anade al usuario al grupo general dentro de la lista de canales.
#Al final inicia un nuevo thread por cada cliente.
def login(socketServer):
    while 1:
        user=list()
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
        aux=canales[0]
        welcome(cliente)
        print "Usuario " + username + " ha entrado al sistema"
        usuarios.append(user)
        canvia_canal(user,"GENERAL")
        x=threading.Thread(target=recibo,args=(cliente,username,direccion,))
        x.start()
#Inicializa el servidor, le pide al usuario el puerto por el cual quiere correr el servicio y genera un socket de conexiones.
def ini_server():
    serverIp = ''
    serverPort = input('Introduce el puerto del servidor:')
    dataConection = (serverIp,serverPort)
    #creamos el socket de conexiones
    socketServer = socket(AF_INET,SOCK_STREAM)
    socketServer.bind(dataConection)

#Funcion principal del programa:
#   Crea una lista de canales en los que el cliente esta a la escucha
#   Crea una variable del canal en el cual el cliente envia los mensajes
#   Se queda a la escucha de los mensajes enviados por el cliente hasta que el cliente envie un EXIT que cierra la conexion
def recibo(cliente,username,direccion,):
    canales_actuales = ["GENERAL"]
    canal_actual = "GENERAL"
    user = list()
    user.append(username)
    user.append(direccion)
    user.append(cliente)
    #Cada respuesta es un comando enviado al servidor, en caso de que el usuario no envie ningun comando,
    #el servidor enviara el mensaje al ultimo grupo al cual se haya conectado el cliente
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
            print respuesta[7:]
            if respuesta[7:] in canales_actuales:
                canal_actual = respuesta[7:]
            else:
                canales_actuales.append(respuesta[7:])
                canal_actual = respuesta[7:]
            canvia_canal(user,respuesta[7:])
            user[2].send("Canal actual: " + canal_actual)
        elif respuesta[:4] == "CREA":
            crea_grupo(respuesta[5:])
            envia(cliente,"CANAL CREADO")
        elif respuesta[:11] == "CANAL_OCULT":
            crea_oculto(respuesta[12:],user)
            envia(cliente,"CANAL OCULTO CREADO")
        elif respuesta[:11] == "ENTRA_OCULT":
            canal_actual = respuesta[12:];
            canales_actuales.append(respuesta[12:])
            canvia_canal_ocult(user,respuesta[12:])
        elif respuesta == "SURT_OCULT":
            canales_actuales.remove(canal_actual)
            surt_grup_ocult(user,canal_actual)
            canal_actual = ""
        elif respuesta == "HELP":
            ayuda(cliente)
        elif respuesta == "EXIT":
            envia(cliente,"EXIT")
            cliente.close()
            print username + " se va!"
            sal_del_sistema(user,canales_actuales)
            exit()
        else:
            for x in range(len(canales)):
                if canal_actual == canales[x][0]:
                    for z in range(len(canales[x])):
                        if z > 0:
                            canales[x][z][2].send(username + " " + respuesta)

#Muestra el contenido del archivo help.txt al cliente, el cual contiene la lista de los comandos que el cliente puede realizar
def ayuda(cliente):
    ayuda = open("help.txt","r")
    for mens in ayuda:
            cliente.send(mens)
    ayuda.close()

#FUncion que borra al usuario de la lista de usuarios del canal oculto
def surt_grup_ocult(user,canal):
    for x in range(len(canales)):
        if ocultos[x][0] == canal:
            ocultos[x].remove(user)
            user[2].send("Has salido del canal")

#Borra al usuario del canal pasado por parametro
def surt_grup(user,canal):
    for x in range(len(canales)):
        if canales[x][0] == canal:
            canales[x].remove(user)
            user[2].send("Has salido del canal")

#Envia un mensaje al cliente pasado por parametro
def envia(cliente,mensaj):
    mensaje = "SERVIDOR: " + str(mensaj)
    cliente.send(mensaje)

#Anade el usuario al canal pasado por parametro a la lista de canales
def canvia_canal(user,canal):
    for x in range(len(canales)):
        if canales[x][0] == canal:
            canales[x].append(user)
            print user[0] + "Anadido al canal: " + canal

def canvia_canal_ocult(user,canal):
    for x in range(len(canales)):
        if ocultos[x][0] == canal:
            ocultos[x].append(user)
            print user[0] + "Anadido al canal: " + canal



#Crea un nuevo canal en la lista de canales
def crea_grupo(nuevo_grupo):
    grupo=list()
    grupo.append(nuevo_grupo)
    canales.append(grupo)

#Crea un nuevo canal oculto en la lista de canales oclutos
def crea_oculto(nuevo_grupo,user):
    grupo = list()
    grupo.append(nuevo_grupo)
    grupo.append(user)
    ocultos.append(grupo)

#FUncion que envia al cliente todos los usuarios que estan conectados al sistema
# por cada grupo
def ver_todos(socketClient):
    print canales
    for x in range(len(canales)):
        for z in range(len(canales[x])):
            if z == 0:
                socketClient.send(canales[x][z])
            else:
                socketClient.send(canales[x][z][0])


#Funcion que envia al cliente todos los canales del servidor
def ver_canales(socketClient):
    for x in range(len(canales)):
        socketClient.send(str(canales[x][0]))

#Envia pide al usuario que introduzca un mensaje para enviar al cliente pasado por parametro
def privado(username,destino,cliente):
    for x in range(len(usuarios)):
        if str(destino) == str(usuarios[x][0]):
            cliente.send("Introduce el mensaje privado:")
            mensaje = cliente.recv(2048)
            mensaje = username + ": " + mensaje
            usuarios[x][2].send(mensaje)

#Envia al cliente todos los usuarios de todos los canales en los que esta a la escucha
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
def sal_del_sistema(user,canales_actuales):
    usuarios.remove(user)
    for x in range(len(canales)):
        for y in range(len(canales_actuales)):
            if canales[x][0] == canales_actuales[y]:
                canales[x].remove(user)

def main():
    #El inicio del codigo hace los mismo que la fincion init()
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
    #Esta parte del main esta dedicada a introducir los comandos desde el servidor:
        #EXIT: CIerra todas las conexiones del servidor
        #CANALS_OCULTS: Muestra un listado de los canales ocultos del servidor
    while on:
        command = raw_input("")
        if command == "EXIT":
            socketClient = socket(AF_INET,SOCK_STREAM)
            socketClient.connect(dataConection)
            socketClient.send("EXIT")
            on=0
            for x in range(len(usuarios)):
                sal_del_sistema(usuarios[0])
        elif command == "CANALS_OCULTS":
            for x in range(len(ocultos)):
                print ocultos[x][0]
    print "GOODBYE!"


main()
