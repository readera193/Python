import argparse, socket
import struct
import sys
import threading
BUFSIZE = 150
CODING = 'UTF-8'

class sendThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        import random
        sendSock, sockname = self.sock.accept()
        data = struct.pack("!H", random.randint(1000,9999))
        sendSock.sendall(data)
        sendSock.close()

def server(host, port):
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listeningSock.bind((host, port))
    listeningSock.listen(1)
    print('Listening at', listeningSock.getsockname())
    
    while True:
        print('Waiting to accept a new connection')
        sock, sockname = listeningSock.accept()
        print('We have accepted a connection from', sockname)
        
        ports = []
        for i in range(4):
            threadSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            threadSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            threadSock.bind((host, 0))
            threadSock.listen(1)
            ports.append(threadSock.getsockname()[1])
            
            send = sendThread(threadSock)
            send.daemon = True
            send.start()
        
        data = struct.pack("!4H", *ports)
        sock.sendall(data)
        sock.close()

def client(host, port):
    sock = connect_to(host, port)
    
    try:
        print(sock.getpeername())
        data = sock.recv(8)
        nums = struct.unpack("!4H", data)
        print(nums)
        sock.close()
        for num in nums:
            sock = connect_to(host, num)
            data = sock.recv(2)
            print("Receiving {} from exam.ipv6.club.tw:{}".format(struct.unpack("!H", data)[0], num))
            sock.close()
    except AttributeError:
        pass
    
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

if __name__ == '__main__':
    choices = {'client':client, 'server':server}
    parser = argparse.ArgumentParser(description='Chat over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=5588,
                        help='TCP port (default 5588)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)