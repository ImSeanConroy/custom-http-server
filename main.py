import socket

HOST = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Listening on {HOST}:{PORT}")

while True:
    client_socket, addr = server_socket.accept()
    print("Connection from", addr)
    client_socket.close()
