import argparse, socket

MAX_BYTES = 65535

def client(port, host):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    text = "1106108136"
    data = text.encode()
    sock.sendto(data, (host, port))
    print('The OS assigned me the address {}'.format(sock.getsockname()))
    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode()
    print('The server {} replied \n{}'.format(address, text))

if __name__ == '__main__':
    choices = {'client': client}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                            ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=62597,
                        help='UDP port (default 62597)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p, args.host)