def client(host, port):
    import xmlrpc.client
    server = xmlrpc.client.ServerProxy('http://{}:{}'.format(host, port))
    
    print(server.login("1106108136"))

def main():
    import argparse
    choices = {'client': client}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=53087,
                        help='TCP port (default 53087)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)

if __name__ == '__main__':
    main()