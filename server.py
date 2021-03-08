import re
import socket

HOST = '127.0.0.1'
PORT = 9000

print(__file__)
curr_dir = re.sub('/$', 'oo', __file__)
print(curr_dir)

# Helper functions
def parse_request(request):
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

# GET method
def http_GET(my_file):
    file = open(my_file, 'r')
    response_body = file.read()

# POST method
def http_POST():
    pass

# DELETE method
def http_DELETE():
    pass

def handle_request(method, my_file):
    if method == 'GET':
        http_GET(my_file)
    elif method == 'POST':
        http_POST(my_file)
    elif method == 'DELETE':
        http_DELETE(my_file)
    else:
        print("error")


# Set up socket
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print(f'Serving HTTP on port {PORT} ...')

# Handle requests
while True:
    connect_socket, client_address = listen_socket.accept()
    request_data = connect_socket.recv(1024).decode('utf-8')
    
    # Parse request
    (request_method,
    request_path,
    request_protocol,
    request_line,
    request_headers,
    request_body) = parse_request(request_data)
    
    # Print request
    print("\n\nRequest accepted!")
    print("LINE:")
    print(f"'{request_line}'")
    print("HEADERS:")
    print(f"'{request_headers}'")
    print("BODY:")
    print(f"'{request_body}'")

    # Get file
    cur_dir = re.sub('/[^/]*$','', __file__)
    if request_path == '/':
        request_path = '/index.html'
    my_file = cur_dir + request_path

    # Implement request methods
    handle_request(request_method)


    if request_method == 'GET':
        http_GET(my_file)
        file = open(my_file, 'r')
        response_body = file.read()
        file.close()

        response_line = 'HTTP/1.1 200 OK\n'
        response_header = 'Content-Type: text/html\n\n'
        http_response = response_line + response_header + response_body

   
   
   
   
    elif request_method == 'POST':
        print(f"\nClient is posting to '{request_path}':")
        print(request_body)
    
    elif request_method == 'DELETE':
        print(f"\nClient is deleting '{request_path}'")
    
    else:
        print("\nHTTP method not recognized. Responding with hello")

#     # Format string
#     request_data = request_data.replace('\n', '<br>')

#     http_response = f"""\
# HTTP/1.1 200 OK

# <html>
#     <head>
#         <title>Hello</title>
#     </head>
#     <body>
#         <h1>Hello from the web!</h1>
#         <h2>Here is the request:</h2>
#         <p>{request_data}</p>
#     </body>
# </html>
# """
    http_response = http_response.encode('utf-8')
    connect_socket.sendall(http_response)
    print("Request fulfilled!")
    connect_socket.close()