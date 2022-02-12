import socket
import threading
from packer import *


class Server():
    def __init__(self):

        self.getIpConfig()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ip, self.port))

        self.client_list = []

    def getIpConfig(self):
        self.ip = input("Type the server IP:\n")
        self.port = int(input("Type the port to be used:\n"))

    def start(self):
        self.s.listen(5)
        print("[SERVER LISTENING CONNECTIONS]")
        while True:
            conn, addr = self.s.accept()
            self.client_list.append(conn)
            newConnection = Connection(self, conn, addr)

            thread = threading.Thread(target=newConnection.handleClient, args=())
            thread.start()

class Connection():

    def __init__(self, server, conn, addr):
        self.server = server
        self.conn = conn
        self.addr = addr
    def sendMessage(self):
        for client in self.server.client_list:
            if self.conn != client:
                try:
                    self.messageFormat(client)
                except:
                    pass
    def messageFormat(self, client):
        message = self.data["message"]
        user = self.data["user"]
        if self.data["info"] == 0:
            client.send(pack({"user": user,
                                    "message": f"[{user}]: {message}"}))
        elif self.data["info"] == 1:
            client.send(pack({"user": user,
                                    "message": f"[NEW USER]{user} entrou no bate-papo!"}))
    def handleClient(self):
        print(f"[NEW CONNECTION] {self.addr} connected.")

        running = True

        while running:
            self.data = unpack(self.conn.recv(2048))
            self.name = self.data["user"]
            self.msg = self.data["message"]
            running = self.handleMessages()
        
        
    def handleMessages(self):
        msg = self.msg.lower()
        if msg.startswith("!exit"):
            self.conn.close()
            return False
        else:
            self.sendMessage()
            return True

server = Server()
server.start()