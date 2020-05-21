import argparse, socket, threading
import struct, time
import sys
BUFSIZE = 150
CODING = 'UTF-8'

def connect_to(hostname_or_ip, port):
    try:
        infolist = socket.getaddrinfo(
          hostname_or_ip, port, 0, socket.SOCK_STREAM, 0,
          socket.AI_ADDRCONFIG | socket.AI_V4MAPPED | socket.AI_CANONNAME,
          )
    except socket.gaierror as e:
        print('Name service failure:', e.args[1])
        sys.exit(1)

    info = infolist[0] # per standard recommendation, try the first one
    socket_args = info[0:3]
    address = info[4]
    sock = socket.socket(*socket_args)
    try:
        sock.connect(address)
    except socket.error as e:
        print('Network failure:', e.args[1])
    else:
        return sock

class recvThread(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
    def run(self):
        sock = connect_to(self.host, self.port)
        data = sock.recv(2)
        number = struct.unpack("!H", data)[0]
        print("Receiving {} from {}:{}".format(number, self.host, self.port))
            
class sendThread(threading.Thread):
    def __init__(self, listeningSock):
        threading.Thread.__init__(self)
        self.listeningSock = listeningSock
    def run(self):
        import random
        sock, sockname = self.listeningSock.accept()
        data = struct.pack("!H", random.randint(0, 9999))
        time.sleep(1)
        sock.sendall(data)
    
def client(host, port):
    sock = connect_to(host, port)
    data = sock.recv(8)
    ports = struct.unpack("!4H", data)
    
    for port in ports:
        recv = recvThread(host, port)
        recv.start()
    sock.close()
    
def server(host, port):
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listeningSock.bind((host, port))
    listeningSock.listen(5)
    print('Listening at', listeningSock.getsockname())
    
    while True:
        sock, sockname = listeningSock.accept()
        ports = []
        for i in range(4):
            lis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            lis.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            lis.bind((host, 0))
            lis.listen(5)

            ports.append(lis.getsockname()[1])
            send = sendThread(lis)
            send.start()
            
        print(ports)
        sock.send(struct.pack("!4H", *ports))
        time.sleep(3)
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