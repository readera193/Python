import argparse, socket
import threading
import pickle
BUFSIZE = 80
EOF = 'oo'

def getInput():
    return input()

def showData(d):
    print('>>', d.decode('UTF-8') ) # align with getInput()

class AsyncRecv(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        while True:
            data = self.sock.recv(BUFSIZE)
            showData(data)

class AsyncSend(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        while True:
            data = getInput()
            self.sock.send( data.encode('UTF-8') )

def server(host, srvPort):
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.bind((host, srvPort))
    listeningSock.listen(1)
    print("Listening at", listeningSock.getsockname() )

    try:
        print("Waiting for incoming calls ...")
        sock, sockname = listeningSock.accept()
        print('We have accepted a connection from', sockname)

        background = AsyncSend(sock)
        background.daemon = True
        background.start()
        while True:
            data = sock.recv(BUFSIZE)
            if not data:
                break
            else:
                showData( data )
        print('Your peer {} closes the connection.'.format(sock.getpeername() ))
        sock.close()
    except KeyboardInterrupt:
        pass
    listeningSock.close()

def client(host, port): # parameter srvPort becomes useless
    # Start chatting
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (host, port) )
    print('Connected to', sock.getpeername() )

    background = AsyncRecv(sock)
    background.daemon = True
    background.start()
    while True:
        msg = getInput()
        if msg == EOF:
            break
        else:
            sock.send( msg.encode('UTF-8') )
    print('I close the socket')
    sock.close()

if __name__ == '__main__':
    choices = {'client': client, 'server': server, }
    parser = argparse.ArgumentParser(description='Chat over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)