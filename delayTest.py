import argparse, socket, multiprocessing, psutil, time

def server(host, port):
    global sum
    info = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0]
    listeningSock = socket.socket( *info[0:3] )
    listeningSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listeningSock.bind( info[4] )
    listeningSock.listen(3)
    print("Listening at", info[4])

    while True:
        sock, sockname = listeningSock.accept()
        proc = multiprocessing.Process(target=handle_connection, args=(sock,))
        proc.start()

def handle_connection(sock):
    usage = psutil.virtual_memory()[2]
    print("[{:4.1f}%] Connecting from {}".format(usage, sock.getpeername()))
    data = sock.recv(50)
    reply = data.decode().upper()
    sock.sendall(reply.encode())
    sock.close()
    print("Reply sent: {}".format(reply))

def client(host, port):
    n = int(input("How many clients? "))
    for i in range(n):
        info = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0]
        sock = socket.socket( *info[0:3] )
        proc = multiprocessing.Process(target=create_connection, args=(sock,info[4]))
        proc.start()
    sock.close()

def create_connection(sock, address):
    sock.connect(address)
    time.sleep(10)
    sock.sendall(b'test')
    reply = sock.recv(50)
    print("Server said: {}".format(reply.decode()))
    sock.close()

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