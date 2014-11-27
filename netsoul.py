#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      AlexMog
#
# Created:     26/11/2014
# Copyright:   (c) AlexMog 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import socket
import hashlib
import time

class NetSoul:
    def __init__(self, server, port, username, password):
        self.server = server
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.authed = 0
        self.username = username
        self.password = password
        self.server_hash = ""
        self.host_client = ""
        self.client_port = ""
        self.timestamp = ""

    def connect(self):
        self.socket.connect((self.server, self.port))

    def send(self, datas):
        print "Sending : " + datas
        self.socket.send(datas + "\n")

    def handle_command(self, line):
        splitter = line.split(" ")
        cmd = splitter[0]
        print "Handling command: " + cmd
        if (cmd == "salut"):
            self.server_hash = splitter[2]
            self.host_client = splitter[3]
            self.client_port = splitter[4]
            self.timestamp = splitter[5]
            self.send("auth_ag ext_user none none")
        elif (cmd == "rep"):
            if (splitter[1] == "002"):
                if (self.authed):
                    self.send("attach")
                    self.send("state actif:" + self.timestamp)
                else:
                    self.authed = 1
                    h = hashlib.md5()
                    h.update(self.server_hash + "-" + self.host_client + "/" + self.client_port + self.password)
                    self.send("ext_user_log " + self.username + " " + h.hexdigest() + " MogClient NULL_OMG")
        elif (cmd == "ping"):
            self.send("ping " + splitter[1])

    def handle(self):
        while 1:
            rep = self.socket.recv(1024)
            if (len(rep) <= 0):
                return ;
            print "Received: " + rep
            self.handle_command(rep)

def main():
    print "Creating instance..."
    # line to modify by the user
    client = NetSoul("163.5.42.2", 4242, "USERNAME", "PASSWORD_SOCKS")
    while 1:
        print "Connecting..."
        client.connect()
        print "Connected!"
        client.handle()
        print "Connexion lost... Reconnecting in 5 seconds..."
        time.sleep(5)

if __name__ == '__main__':
    main()