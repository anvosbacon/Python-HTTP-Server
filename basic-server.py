import socket

HOST = ''
PORT = 9000

# Set up socket
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print(f'Serving HTTP on port {PORT} ...')

# Handle requests
while True:
    connect_socket, client_address = listen_socket.accept()
    request_data = connect_socket.recv(1024)
    print(request_data.decode('utf-8'))

    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    connect_socket.sendall(http_response)
    connect_socket.close()
