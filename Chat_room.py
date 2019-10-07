import argparse, socket
import threading
import json
BUFSIZE = 80
REGISTRAR_PORT = 648
EOF = 'oo'
SOCKS = {}

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
            
class serverThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        sock = self.sock
        while True:
            data = sock.recv(BUFSIZE).decode('UTF-8')
            if data[0] == '/':
                data = data.split()
                if len(data)==2 and (data[0]=="/USER" or data[0]=="/user"):
                    SOCKS[sock] = data[1]
                else:
                    sock.sendall(b'error')
            # TODO: search sock by get()
            elif sock in SOCKS.values():
                print(otherdata)
                for otherSock, otherName in SOCKS.items():
                    if otherSock != sock:
                        otherSock.sendall(otherName+' : '+otherSock)
            else:
                sock.sendall(b"Usage: /user <userName>")
        sock.close()

def server(host, port):
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.bind((host, port))
    listeningSock.listen(1)
    while True:
        print('Waiting to accept a new connection')
        sock, sockname = listeningSock.accept()
        print('We have accepted a connection from', sockname)
        thread = serverThread(sock)
        thread.daemon = True
        thread.start()
    
def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Connected to", sock.getpeername())
    
    recv = recvThread(sock)
    recv.start()
    send = sendThread(sock)
    send.start()
    recv.join()
    send.join()
    sock.close()
    
if __name__ == '__main__':
    choices = {'client':client, 'server':server}
    parser = argparse.ArgumentParser(description='Chat over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=8136,
                        help='TCP port (default 8136)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)