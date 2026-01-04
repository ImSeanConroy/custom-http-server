import socket

HOST = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

while True:
    client_socket, addr = server_socket.accept()
    print("Connection from", addr)

    response = "HTTP/1.1 200 OK\r\n\r\n"
    client_socket.sendall(response.encode())

    client_socket.close()
