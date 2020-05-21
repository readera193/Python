#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter02/udp_local.py
# UDP client and server on localhost

import argparse, socket
import time
from datetime import datetime

MAX_BYTES = 65535
banana = [
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWWWNNNNWMMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWWNNNXXK00KWMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWWNNNNXK00OkKWMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWWNNNXK0Okxk0NMMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWWWWNNXXK0OkkOXWMMMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWWWWNNNK0OOkk0NMMMMMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWWNNNXX0Okxk0WMMMMMMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWWWNNNX0Okxx0WMMMMMMMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWWWNNXK0OxxOXMMMMMMMMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWNNNNNXKOkxxKWMMMMMMMMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWNNNNXK0OxdkXMMMMMMMMMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWNNNNNXK0OxdkXMMMMMMMMMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWNXXNNX00kddkXMMMMWWWWMMMMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMMMMMWWNNXXNNNWWWWNXXXXX00kddkKNNNX0kk0XNWMMMMMMMMMMMMMM',
    'MMMMMMMMMMMMMMMWNX000KK00O0KXNNNNNXXXK0OkddxxxxkkkxkO0KXNWMMMMMMMMMMMM',
    'MMMMMMMMMMMMMWNKOOKNWWWWWXXNNNNNNNK0OxxkkddxxxxxkkOO0KXXKXNWWMMMMMMMMM',
    'MMMMMMMMMMMMNKOOKWWMMMWNXKXNNNNXXKkdoloddoodxddddx00kkO0KKKKXNWMMMMMMM',
    'MMMMMMMMWWWXOk0NMMMMMMWXKKXNNNNXXkollllllccoooood0WWNKOOO00K00XWMMMMMM',
    'MMMMMMMMMWXOkKWMMMMMMMNK0KXNNNNN0dllllclc::cllllkNMMMMWNX0OO0OOKNMMMMM',
    'MMMMMMMMWKkkXWMMMMMMMWXKKKXNNNNXOdlllccc::;:ccclkWMMMMMMMWXOOOOO0NMMMM',
    'MMMMMMMNKkOXWMMMMMMMMWX0KXNXNNNKkdoollcc::::::ccxNMMMMMMMMMN0kkOO0NMMM',
    'MMMMMWX0O0NMMMMMMMMMMWX0KXNXNNNKOkdoollcc:::::ccoKWMMMMMMMMMWKOkkkKWMM',
    'WWWWNK00XWMMMMMMMMMMMWXKKXXXNNNK00kdoolcccccc:cclkWMMMMMMMMMMMN0kkXMMM',
    '0OOO0KNWMMMMMMMMMMMMMWNKKXXXNNNXOKKxdoolcccccccccxNMMMMMMMMMMMMWNNWMMM',
    'K0KXWWWMMMMMMMMMMMMMMMNXKKXXXNNXK0XN0xdllccccccccdXMMMMMMMMMMMMMMMMMMM',
    'MMMMMMWMMMMMMMMMMMMMMMWXKKXXXXXXXOKMNOdolccccccccdKMMMMMMMMMMMMMMMMMMM',
    ]

def server(port, host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))
        text = 'Your data was {} bytes long'.format(len(data))
        data = text.encode('ascii')
        sock.sendto(data, address)

def client(port, host):
    for text in banana:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = text.encode('ascii')
        sock.sendto(data, (host, port))
        print('The OS assigned me the address {}'.format(sock.getsockname()))
        data, address = sock.recvfrom(MAX_BYTES)  # Danger! See Chapter 2
        text = data.decode('ascii')
        print('The server {} replied {!r}'.format(address, text))
        time.sleep(0.1)

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
