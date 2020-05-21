import argparse, socket

MAX_BYTES = 65535

ID = ['']

def client(port, host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = "1106108136"
    data = text.encode()
    sock.sendto(data, (host, port))
    print('The OS assigned me the address {}'.format(sock.getsockname()))
    data, address = sock.recvfrom(MAX_BYTES)  # Danger! See Chapter 2
    text = data.decode()
    print('The server {} replied {!r}'.format(address, text))
    
def server(port, host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        student_id = data.decode()
        if student_id in ID:
            text = "{} has already logged in as the {}nd student.".format(student_id, ID.index(student_id))
        else:
            text = "Welcome, {}, you're the {}nd to login.".format(student_id, len(ID))
            ID.append(student_id)
            
        print(text)
        data = text.encode()
        sock.sendto(data, address)

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                            ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p, args.host)