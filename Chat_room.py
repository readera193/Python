import argparse, socket
import threading
BUFSIZE = 80
IRC_PORT = 6667
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
            args = msg.split()
            if len(args)==1 and args[0].upper()=="/QUIT":
                break
            
class serverThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        sock = self.sock
        # TODO: 使用者非使用指令離開/意外斷線時，需移除SOCKS內容
        while True:
            data = sock.recv(BUFSIZE).decode('UTF-8')
            args = data.split()
            if data[0]=='/':
                if len(args)==2 and args[0].upper()=="/USER":
                    if sock not in SOCKS.keys():
                        print("User [{}\t] joined".format(args[1]))
                    else:
                        print("User [{}\t] rename as [{}\t]".format(SOCKS[sock], args[1]))
                    SOCKS[sock] = args[1]
                elif len(args)==1 and args[0].upper()=="/WHO":
                    for name in SOCKS.values():
                        msg = "User [{}\t] is online".format(name)
                        sock.sendall(msg.encode('UTF-8'))
                elif len(args)==1 and args[0].upper()=="/QUIT":
                    name = SOCKS.pop(sock)
                    print("User [{}\t] left".format(name))
                    break
                else:
                    sock.sendall(b'Incorrect command')
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
    print("Listening at", listeningSock.getsockname())
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