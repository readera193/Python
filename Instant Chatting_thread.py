import argparse, socket
import threading
BUFSIZE = 80
EOF = 'oo'

class threadRecv(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        while True:
            data = self.sock.recv(BUFSIZE)
            print(">>", data.decode('UTF-8'))

class threadSend(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        while True:
            msg = input()
            self.sock.sendall(msg.encode('UTF-8'))

def server(host, port):
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.bind((host, port))
    listeningSock.listen(1)
    print("Listening at", listeningSock.getsockname())
    
    sock, sockname = listeningSock.accept()
    print("We have accepted a connection from", sockname)
    
    recv = threadRecv(sock)
    recv.start()
    send = threadSend(sock)
    send.start()
    
    recv.join()
    send.join()
    print("Your peer {} closes the connection.".format(sock.getpeername() ))
    sock.close()
    listeningSock.close()
    
def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Connected to", sock.getpeername())
    
    recv = threadRecv(sock)
    recv.start()
    send = threadSend(sock)
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
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)