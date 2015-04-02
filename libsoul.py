import socket
import hashlib
import time
import urllib
import traceback

DEBUG = 0

class user:
    def __init__(self):
        self.socket = ""
        self.trust_level = ""
        self.login = ""
        self.user_host = ""
        self.workstation_type = ""
        self.location = ""
        self.group = ""
        self.status = ""
        self.state = ""
        self.state_timestamp = ""


class NetsoulApi:
    def __init__(self, server, port, username, password, location):
        self.server = server
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.authed = 0
        self.username = username
        self.password = password
        self.socket_num = ""
        self.server_hash = ""
        self.host_client = ""
        self.port_client = ""
        self.server_timestamp = ""
        self.state = "actif"
        self.client = "LibPyNetsoul"
        self.location = location
        self.listeners = []
        self.conn_status = 0

    def add_listener(self, listener):
        self.listeners.append(listener)

    def connect(self):
        self.socket.connect((self.server, self.port))
        self.conn_status = 1

    def sendcmd(self, cmd):
        if DEBUG:
            print ">> " + cmd
        self.socket.send(cmd + "\n")

    def handle_cmd(self, data):
        args = data.split(" ")
        cmd = "_" + args[0]
#        try:
        fnc = getattr(self, cmd)
        fnc(args)
#        except Exception, e:
#            self.handle_error(e)

    def handle_error(self, ex):
        print ex
        traceback.print_exc()

    def handle_data(self):
        while 1:
            rep = self.socket.recv(1024)
            if (len(rep) <= 0):
                disconnect()
                break
            if DEBUG:
                print "<< " + rep
            try:
                self.handle_cmd(rep)
            except Exception, e:
                self.handle_error(e)

    def disconnect(self):
        self.conn_status = 0
        for listener in self.listeners:
            try:
                listener.on_disconnect()
            except:
                pass
        self.socket.disconnect();

    def send_exit(self):
        self.sendcmd("exit")

    """ states possible:
    actif: You are on your PC!
    away: You are away :(
    connection: Default status for conneciton.
    idle: You are not locked but you don't move... Are you dead?!
    lock: You are locked.
    server: You're a server? COOL!
    none: You don't want to use a status :( """
    def send_state(self, state):
        self.state = state
        self.sendcmd("user_cmd state " + state)

    def send_msg(self, to, msg):
        self.sendcmd("user_cmd msg_user " + to + " msg " + urllib.urlencode(msg))
    
    def send_watch_log_user(self, user):
        self.sendcmd("user_cmd watch_log_user " + user)

    def send_who(self, user):
        self.sendcmd("user_cmd who " + user)
    
    # commands section
    def _salut(self, args):
        self.socket_num = args[1]
        self.server_hash = args[2]
        self.host_client = args[3]
        self.port_client = args[4]
        self.server_timestamp = args[5]
        self.sendcmd("auth_ag ext_user none none")
        self.conn_status = 2
        for listener in self.listeners:
            try:
                listener.on_salut()
            except:
                pass

    def _rep(self, args):
        if (args[1] == "002"):
            if (self.authed):
#                self.sendcmd("attach")
                self.send_state("actif")
                if self.conn_status == 3:
                    for listener in self.listeners:
                        try:
                            listener.on_authed()
                        except:
                            pass
                self.conn_status = 4
            else:
                self.authed = 1
                h = hashlib.md5()
                client = urllib.quote_plus(self.client)
                location = urllib.quote_plus(self.location)
                h.update(self.server_hash + "-" + self.host_client + "/" + self.port_client + self.password)
                self.sendcmd("ext_user_log " + self.username + " " + h.hexdigest() + " "
                             + client + " " + location)
                self.conn_status = 3
                for listener in self.listeners:
                    try:
                        listener.on_auth_request_sended()
                    except:
                        pass

    def _ping(self, args):
        self.sendcmd("ping " + args[1])

    #TODO: cmds: WHO
    def _user_cmd(self, args):
        tab = args[1].split(":")
        if tab[1] == "user":
            u = user()
            user.socket = tab[0]
            u.trust_level = tab[2]
            addr = tab[3].split("@")
            u.login = addr[0]
            u.user_host = addr[1]
            u.workstation_type = tab[4]
            u.location = tab[5]
            u.group = tab[6]
            u.status = args[3]
            if status == "state":
                u.status = "login"
                status_cut = args[4].split(":")
                u.state = status_cut[0]
                u.state_timestamp = status_cut[1]
                for listener in self.listeners:
                    try:
                        listener.on_user_state_changed(u)
                    except:
                        pass
            elif status == "msg":
                msg = args[4]
                for listener in self.listeners:
                    try:
                        listener.on_user_msg(u, msg)
                    except:
                        pass
                
