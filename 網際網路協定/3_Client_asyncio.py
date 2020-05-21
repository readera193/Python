import argparse, socket, asyncio

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
    address = (args.host, args.p)
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(server_1, *address)
    loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Stopping server')
    finally:
        loop.close()

async def server_1(reader, writer):
    global sum
    address = writer.get_extra_info('peername')
    print('Accepted connection from {}'.format(address))
    while True:
        data = b''
        
        more_data = await reader.read(1)
        if not more_data:
            if data:
                print('Client {} sent {!r} but then closed'
                      .format(address, data))
            else:
                print('Client {} closed socket normally'.format(address))
            return
        data += more_data
        
        n = int(data.decode())
        print("{} + {}".format( sum, n), end='')
        sum += n
        print(" = {}".format(sum) )

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