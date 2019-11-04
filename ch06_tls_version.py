import socket
import ssl

hostname = 'www.google.com'
context = ssl.create_default_context()
address = (hostname, 443)
with socket.create_connection(address) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(ssock.version())

cert = ssl.get_server_certificate(address)
print(cert)
