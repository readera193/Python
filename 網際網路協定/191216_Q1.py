import argparse, socket

QUESTION = '''
1. The server is listening at exam.ipv6.club.tw:8565 with UDP.
2. If a client sends a string of student ID (actually, a bytes array,
   such as b"1106108123") to the server, the server will reply a
   message.
3. If the student ID belongs to a student enrolled to this class,
   the server will reply the name of the student.'''

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    reply = sock.recv(500)
    print(reply.decode())
    sock.close()
    
def server(interface, port):
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listeningSock.bind((interface, port))
    listeningSock.listen(1)
    print('Listening at', listeningSock.getsockname())
    
    while True:
        print('Waiting to accept a new connection')
        sock, sockname = listeningSock.accept()
        print('We have accepted a connection from', sockname)
        print('  Socket name:', sock.getsockname())
        print('  Socket peer:', sock.getpeername())
        sock.sendall(QUESTION.encode())
        sock.close()

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
