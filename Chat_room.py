import argparse, socket
import threading
BUFSIZE = 150
IRC_PORT = 6667
SOCKS = {}      # {username=>sock}
ERROR_MSG = "Incorrect command, usage of commands:\n"+\
            "Set username/Rename: /user <username>\n"+\
            "Get users who logged into the server: /who\n"+\
            "Quit: /quit"

class recvThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        while True:
            data = self.sock.recv(BUFSIZE)
            print(data.decode('UTF-8'))

class sendThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        while True:
            msg = input()
            self.sock.sendall(msg.encode('UTF-8'))
            args = msg.split()
            if args[0].lower()=="/quit" and len(args)==1:
                break
            
class serverThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.username = None
    def run(self):
        try:
            while True:
                data = self.sock.recv(BUFSIZE).decode('UTF-8')
                if data[0]=='/':
                    args = data.split()
                    if args[0].lower()=="/user":
                        self.setUsername(args)
                    elif args[0].lower()=="/who" and len(args)==1:
                        if len(SOCKS) > 0:
                            for username in SOCKS.keys():
                                msg = "User [{}\t] is online".format(username)
                                self.sock.sendall(msg.encode('UTF-8'))
                        else:
                            self.sock.sendall(b"No user is online")
                    elif args[0].lower()=="/quit" and len(args)==1:
                        self.userQuit()
                        break
                    else:
                        self.sock.sendall(ERROR_MSG.encode('UTF-8'))
                elif self.username != None:
                    print(self.username, " : ", data)
                    for otherSocks in SOCKS.values():
                        if otherSocks != self.sock:
                            otherSocks.sendall((self.username+" : "+data).encode('UTF-8'))
                else:
                    self.sock.sendall(b"Please set yout username to chat, Usage: /user <userName>")
        except ConnectionResetError:
            self.userQuit()
        self.sock.close()
    def setUsername(self, args):
        if len(args) != 2:
            self.sock.sendall(b"Incorrect command, Usage: /user <userName>")
            return
        if args[1] in SOCKS.keys():
            self.sock.sendall(b"This username has already been used")
            return
        if self.username == None:
            print("User [{}\t] joined".format(args[1]))
        else:
            print("User [{}\t] rename as [{}\t]".format(self.username, args[1]))
            SOCKS.pop(self.username)
        self.username = args[1]
        SOCKS[self.username] = self.sock
    def userQuit(self):
        if self.username != None:
            print("User [{}\t] left".format(self.username))
            SOCKS.pop(self.username)

def server(host, port):
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.bind((host, port))
    listeningSock.listen(1)
    print("Listening at", listeningSock.getsockname())
    while True:
        sock, sockname = listeningSock.accept()
        sock.sendall(b"Please set yout username, Usage: /user <userName>")
        thread = serverThread(sock)
        thread.daemon = True
        thread.start()
    
def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Connected to", sock.getpeername())
    
    recv = recvThread(sock)
    recv.daemon = True
    recv.start()
    send = sendThread(sock)
    send.start()
    
    send.join()
    sock.close()
    
if __name__ == '__main__':
    choices = {'client':client, 'server':server}
    parser = argparse.ArgumentParser(description='Chat over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=IRC_PORT,
                        help='TCP port (default 6667)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)