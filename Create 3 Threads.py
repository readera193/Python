import argparse, socket, threading

def client(host, port):
    info = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0]
    sock = socket.socket( *info[0:3] )
    sock.connect( info[4] )
    for i in range(3):
        n = input("? ")
        sock.send( n.encode() )
    sock.close()

def server(host, port):
    global sum
    info = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0]
    listeningSock = socket.socket( *info[0:3] )
    listeningSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listeningSock.bind( info[4] )
    listeningSock.listen(3)
    print("Listening at", info[4])

    threadList = []
    for i in range(3):
        sock, sockname = listeningSock.accept()
        print("Connecting from", sockname)
        serverThread = threading.Thread(target=server_1, args=(sock,))
        serverThread.start()
        threadList.append(serverThread)

    for thread in threadList:
        thread.join()
    print(sum)

def server_1(s):
    global sum
    for i in range(3):
        data = s.recv(1)
        n = int(data.decode())
        print("{} + {}".format( sum, n), end='')
        sum += n
        print(" = {}".format(sum) )
    s.close()

if __name__ == '__main__':
    global sum
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Chat over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    sum = 0
    function(args.host, args.p)