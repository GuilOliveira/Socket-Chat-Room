from multiprocessing.connection import Client
import socket
from packer import *
import threading

class Client:

    def __init__(self):

        self.getIpConfig()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.ip, self.port))
        self.Connected = True

        
        self.name = self.initialConfig()

        self.send = threading.Thread(target=self.sendToServer, args=(self.name, ))
        self.receive = threading.Thread(target=self.receiveFromServer)
        self.send.start()
        self.receive.start()
        print("Welcome! type !exit to quit")

    def sendMessage(self, name, msg, info = 0):
        data = {"user": name,
                "message": str(msg),
                "info": info}
        self.client.send(pack(data))
    
    def getIpConfig(self):
        self.ip = input("Type the server IP:\n")
        self.port = int(input("Type the port to be used:\n"))

    def sendToServer(self, name):
        while self.Connected:
            msg = self.rmvUselessSpaces(input())
            if msg!="":
                self.sendMessage(name, msg)
            if msg.lower() == "!exit":
                self.Connected = False
    def rmvUselessSpaces(self, msg):
        msg = list(msg)
        i = 0
        msgLength = len(msg)
        while i < msgLength:
            if (msg[i] == "") or (msg[i] == " "):
                del(msg[i])
                msgLength-=1
                i=-1
            else:
                return ''.join(msg)
            i+=1
        return ''.join(msg)

    def receiveFromServer(self):
        while self.Connected:
            try:
                msg = unpack(self.client.recv(2048))
                print(msg["message"])
            except:
                pass


    def initialConfig(self):
        name = input("Enter your name:\n")
        self.sendMessage(name, "", 1)
        return name

client = Client()

