import argparse, socket
import threading
import logging
BUFSIZE = 80
EOF = 'oo'
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
flagToExit = threading.Event()

def getInput():
    return input()

def showData(d):
    print('>>', d) # align with getInput()

class AsyncRecv(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        try:
            while True:
                data = self.sock.recv(BUFSIZE).decode('UTF-8')
                showData(data)
        except ConnectionResetError:
            print('Your peer {} closes the connection.'.format(self.sock.getpeername() ))
            print('Input anything to exit.')
            flagToExit.set()

class AsyncSend(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self):
        while True:
            msg = getInput()
            if flagToExit.is_set():
                break
            if msg==EOF:
                print('I close the socket')
                break
            else:
                self.sock.send( msg.encode('UTF-8') )

def createThreads(sock):
    sendThread = AsyncSend(sock)
    recvThread = AsyncRecv(sock)
    sendThread.daemon = True
    recvThread.daemon = True
    sendThread.start()
    recvThread.start()

    sendThread.join()

def server(host, srvPort):
    listeningSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSock.bind((host, srvPort))
    listeningSock.listen(1)
    print("Listening at", listeningSock.getsockname() )

    print("Waiting for incoming calls ...")
    sock, sockname = listeningSock.accept()
    print('We have accepted a connection from', sockname)

    createThreads(sock)
    sock.close()
    
    listeningSock.close()

def client(host, port): # parameter srvPort becomes useless
    # Start chatting
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (host, port) )
    print('Connected to', sock.getpeername() )

    createThreads(sock)
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