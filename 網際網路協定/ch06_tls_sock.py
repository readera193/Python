import argparse, ssl, socket

def main():
    parser = argparse.ArgumentParser(description='send/recv over TLS')
    parser.add_argument('host', help='hostname or IP address')
    parser.add_argument('-c', metavar='cafile', default=None,
                        help='run as client: path to CA certificate PEM file')
    parser.add_argument('-s', metavar='certfile', default=None,
                        help='run as server: path to server PEM file')
    parser.add_argument('-p', metavar='port', default=1060,
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

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (host,port) )
    print("Connected to host {} at port {}".format(host, port) )
    ssock = context.wrap_socket(sock, server_hostname=host)
    data = ssock.recv(1024)
    print(data.decode())
    ssock.close()
    sock.close()

def server(host, port, certfile):
    purpose = ssl.Purpose.CLIENT_AUTH
    context = ssl.create_default_context(purpose)
    context.load_cert_chain(certfile)

    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listeningSock.bind( (host, port) )
    listeningSock.listen(1)
    print("Listening at {}:{}".format(host, port))
    sock, address = listeningSock.accept()
    print("Connection from {}:{}".format(*address))
    ssock = context.wrap_socket(sock, server_side=True)

    ssock.sendall('Simple is better than complex.'.encode())
    ssock.close()
    listeningSock.close()

if __name__ == "__main__":
    main()

