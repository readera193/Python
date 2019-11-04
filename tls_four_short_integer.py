import argparse, socket
import struct
import sys
import ssl
BUFSIZE = 150
CODING = 'UTF-8'

def main():
    parser = argparse.ArgumentParser(description='send/recv over TLS')
    parser.add_argument('host', help='hostname or IP address')
    parser.add_argument('-c', metavar='cafile', default=None,
                        help='run as client: path to CA certificate PEM file')
    parser.add_argument('-s', metavar='certfile', default=None,
                        help='run as server: path to server PEM file')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='port number (default: 1060)')
    args = parser.parse_args()
    if args.s and args.c:
        parser.error('you cannot specify both -c and -s')
    elif args.s:
        server(args.host, args.p, args.s)
    else:
        client(args.host, args.p, args.c)

def client(host, port, cafile=None):
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile=cafile)
    context.check_hostname = False
    
    sock = connect_to(host, port)
    ssock = context.wrap_socket(sock, server_hostname=host)
    
    try:
        print(ssock.getpeername())
        data = ssock.recv(8)
        print(struct.unpack("!4H", data))
        ssock.close()
    except AttributeError:
        pass

def server(host, port, certfile):
    numbers = (6666, 7777, 8888, 9999)
    
    purpose = ssl.Purpose.CLIENT_AUTH
    context = ssl.create_default_context(purpose)
    context.load_cert_chain(certfile)
    
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listeningSock.bind((host, port))
    listeningSock.listen(1)
    print('Listening at', listeningSock.getsockname())
    
    while True:
        print('Waiting to accept a new connection')
        sock, sockname = listeningSock.accept()
        
        ssock = context.wrap_socket(sock, server_side=True)
        print('We have accepted a connection from', sockname)
        data = struct.pack("!4H", *numbers)
        ssock.sendall(data)

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

if __name__ == '__main__':
    main()