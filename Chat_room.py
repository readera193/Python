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
            args = data.split()
            if data[0]=='/':
                if len(args)==2 and args[0].lower()=="/user":
                    SOCKS[sock] = args[1]
                    print("User {} joined".format(args[1]))
                else:
                    sock.sendall(b'error')
            elif sock in SOCKS.keys():
                print(SOCKS[sock], " : ", data)
                for otherSocks in SOCKS.keys():
                    if otherSocks != sock:
                        otherSocks.sendall((SOCKS[sock]+" : "+data).encode('UTF-8'))
            else:
                sock.sendall(b"Usage: /user <userName>")
        sock.close()

def server(host, port):
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.bind((host, port))
    listeningSock.listen(1)
    while True:
        sock, sockname = listeningSock.accept()
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