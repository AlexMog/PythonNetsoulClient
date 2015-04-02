#!/usr/bin/env python
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

from libsoul import *

class NetSoulClient:
    def __init__(self, server, port, username, password, location):
        self.api = NetsoulApi(server, port, username, password, location)

    def start(self):
        print "Connecting to server..."
        self.api.connect()
        print "Connected."
        self.api.add_listener(self)
        print "Listening started."
        self.api.handle_data()
    
    def on_disconnect(self):
        print "Disconnected."

    def on_salut(self):
        print "Authentication demand received."

    def on_auth_request_sended(self):
        print "Auth request sended."

    def on_user_state_changed(self, user):
        print "UserStateChanged: " + user.login + "@" + user.location + " : " + user.status

    def on_user_msg(self, user, msg):
        print "Received a message from: " + user.login + "@" + user.location + " : " + msg

    def on_authed(self):
        print "Authentication successful!"

def main():
    # line to modify by the user
    client = NetSoulClient("163.5.42.2", 4242, "CLIENT_LOGIN", "CLIENT_PASS", "LOCATION")
    client.start()

if __name__ == '__main__':
    main()
