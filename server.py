import os
import re
import socket

HOST = '127.0.0.1'
PORT = 9000

class my_webserver:
    def __init__(self, host, port):
        self.listen_socket = listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((host, port))
        listen_socket.listen(1)
        print(f'Serving HTTP on port {PORT} ...')
    
    def run(self):
        while True:
            self.connect_socket, self.client_address = self.listen_socket.accept()
            self.request_data = self.connect_socket.recv(1024).decode('utf-8')

            # Parse request
            (self.request_method,
            self.request_path,
            self.request_protocol,
            self.request_line,
            self.request_headers,
            self.request_body) = self.parse_request(self.request_data)

            # Get file
            directory = os.path.dirname(__file__)
            if self.request_path == '/':
                self.request_file = directory + '/index.html'
            else:
                self.request_file = directory + self.request_path

            # Print request in console
            print("\n\nRequest accepted!")
            print("LINE:")
            print(f"'{self.request_line}'")
            print("HEADERS:")
            print(f"'{self.request_headers}'")
            print("BODY:")
            print(f"'{self.request_body}'")

            # Build response
            http_response = self.build_response()
            print('exited response')
            print('Response:')

            # # Build test response
            # http_response = self.build_placeholder_response()

            print(http_response)

            

            # Send response
            self.connect_socket.sendall(http_response)
            print("Request fulfilled!")
            self.connect_socket.close()
    
    def parse_request(self, request):
        split_1 = request.split('\r\n', 1)
        line = split_1[0]

        split_2 = split_1[1].split('\r\n\r\n', 1)
        headers = split_2[0]
        body = split_2[1]

        split_3 = line.split(' ')
        method = split_3[0]
        path = split_3[1]
        protocol = split_3[2]

        return method, path, protocol, line, headers, body

    def build_response(self):
        print("entered response")
        response = None
        if self.request_method == 'GET':
            response = self.build_GET()
        elif self.request_method == 'POST':
            response = self.build_POST()
        elif self.request_method == 'DELETE':
            response = self.build_DELETE()
        else:
            response = f"""\
HTTP/1.1 400 Bad Request
Content-Type: text/html; charset=utf-8

<html>
    <head>
        <title>Error</title>
    </head>
    <body>
        <h1>HTTP/1.1 400 Bad Request</h1>
    </body>
</html>
"""
            print("I'm still in the indent")
            response = response.encode('utf-8')
        return response
        
    def build_placeholder_response(self):
        formatted_request = self.request_data.replace('\n', '<br>')
        response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<html>
    <head>
        <title>Hello</title>
    </head>
    <body>
        <h1>Hello from the web!</h1>
        <h2>Here is the request:</h2>
        <p>{formatted_request}</p>
    </body>
</html>
"""
        return response.encode('utf-8')
    
    def build_GET(self):
        file = open(self.request_file, 'rb')
        body = file.read()
        file.close()

        header = 'HTTP/1.1 200 OK\n'

        if self.request_file.endswith('.jpg'):
            mimetype = 'image/jpg'
        elif self.request_file.endswith('.png'):
            mimetype = 'image/png'
        elif self.request_file.endswith('.ico'):
            mimetype = 'image/vnd.microsoft.icon'
        elif self.request_file.endswith('.css'):
            mimetype = 'text/css'
        else:
            mimetype = 'text/html; charset=utf-8'
        
        header += 'Content-type: ' + mimetype + '\n\n'
        return header.encode('utf-8') + body

    def build_POST(self):
        post = re.sub('^.*=', '', self.request_body)
        print(post)
        return self.build_placeholder_response()

    def build_DELETE(self):
        return self.build_placeholder_response()

server = my_webserver(HOST, PORT)
server.run()