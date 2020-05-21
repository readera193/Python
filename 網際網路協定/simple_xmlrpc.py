def f(a, b):
    return a+b

def client(host, port):
    import xmlrpc.client
    server = xmlrpc.client.ServerProxy('http://{}:{}'.format(host, port))
    print(server.f(7, 70))

def server(host, port):
    from xmlrpc.server import SimpleXMLRPCServer
    server = SimpleXMLRPCServer((host, port))
    server.register_function(f)
    server.serve_forever()

def main():
    import argparse
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

if __name__ == '__main__':
    main()