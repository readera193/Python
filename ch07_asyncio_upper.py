#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_asyncio2.py
# Asynchronous I/O inside an "asyncio" coroutine.

import argparse
import socket
import asyncio

def client(address):
    host , port = address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    s = input('? ')
    sock.sendall(s.encode())
    reply = sock.recv(128)
    print('The server said', repr(reply))
    sock.close()

def server(address):
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_conversation, *address)
    loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Stopping server')
    finally:
        loop.close()

def get_answer(data):
    d = data.decode().upper().encode()
    return d

async def handle_conversation(reader, writer):
    address = writer.get_extra_info('peername')
    print('Accepted connection from {}'.format(address))
    while True:
        data = b''

        more_data = await reader.read(4096)
        if not more_data:
            if data:
                print('Client {} sent {!r} but then closed'
                      .format(address, data))
            else:
                print('Client {} closed socket normally'.format(address))
            return
        data += more_data

        answer = get_answer(data)
        writer.write(answer)

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    description = 'asyncio server using coroutine'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    function = choices[args.role]
    function(address)
