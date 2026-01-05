import socket
import threading

HOST = "127.0.0.1"
PORT = 8080

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    request_line = request.splitlines()[0]
    method, path, version = request_line.split()

    print("Method:", method)
    print("Path:", path)
    print("Version:", version)

    headers = {}
    for line in request.splitlines()[1:]:
        if line == "":
            break
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()

    print("Headers:", headers)

    body = ""
    if "content-length" in headers:
        length = int(headers["content-length"])
        body = client_socket.recv(length).decode()

    print("Body:", body)

    body = f"Path: {path}\nBody: {body}"
    response = (
        "HTTP/1.1 200 OK\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        f"{body}"
    )

    client_socket.sendall(response.encode())
    client_socket.close()

if __name__ == "__main__":

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        print("===================")
        print("Connection Address:", addr[0])
        print("Connection Port:", addr[1])

        threading.Thread(target=handle_client, args=(client_socket,)).start()
        
        