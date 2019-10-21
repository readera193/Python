import argparse, socket
import struct
BUFSIZE = 150
CODING = 'UTF-8'
    
def client(host, port):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(sock.getpeername())
    
    data = sock.recv(8)
    for i in range(0, 8, 2):
        print(struct.unpack("!H", data[i:i+2]))
    sock.close()
    
if __name__ == '__main__':
    choices = {'client':client}
    parser = argparse.ArgumentParser(description='Chat over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 6667)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)