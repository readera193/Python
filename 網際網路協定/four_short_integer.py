import argparse, socket
import struct
import sys
BUFSIZE = 150
CODING = 'UTF-8'
    
def client(host, port):
    sock = connect_to(host, port)
    
    try:
        print(sock.getpeername())
        data = sock.recv(8)
        print(struct.unpack("!4H", data))
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
        print('Success')
        return sock

def server(host, port):
    numbers = (6666, 7777, 8888, 9999)
    
    listeningSock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    listeningSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listeningSock.bind((host, port))
    listeningSock.listen(1)
    print('Listening at', listeningSock.getsockname())
    
    while True:
        print('Waiting to accept a new connection')
        sock, sockname = listeningSock.accept()
        print('We have accepted a connection from', sockname)
        data = struct.pack("!4H", *numbers)
        sock.sendall(data)

if __name__ == '__main__':
    choices = {'client':client, 'server':server}
    parser = argparse.ArgumentParser(description='Chat over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 6667)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)