import socket
import threading
from typing import Dict, Tuple


class HttpServer:

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8080,
        buffer_size: int = 1024,
        response_timeout: int = 5
    ):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.response_timeout = response_timeout

    # -------------------------------
    # HTTP helpers
    # -------------------------------
    def send_response(self, client_socket: socket.socket, status_code: int, body: str) -> None:
        """
        Send an HTTP response to the client.

        Args:
            socket (socket.socket): The client socket.
            status_code (int): HTTP status code (e.g. 200, 400, 500).
            body (str): Response body text.

        Returns:
            None
        """
        status_messages = { 200: "OK", 400: "Bad Request", 500: "Internal Server Error" }
        status_text = status_messages.get(status_code, "OK")
        body_bytes = body.encode("utf-8")

        response = (
            f"HTTP/1.1 {status_code} {status_text}\r\n"
            f"Content-Length: {len(body_bytes)}\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode() + body_bytes

        client_socket.sendall(response)

    def parse_headers(self, lines) -> Dict[str, str]:
        """
        Parse HTTP headers into a dictionary.

        Args:
            lines (Iterable[str]): Raw HTTP header lines.

        Returns:
            Dict[str, str]: A dictionary containing parsed HTTP headers.
        """
        headers = {}

        for line in lines:
            if not line:
                break
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            headers[key.lower().strip()] = value.strip()

        return headers 

# -------------------------------
# Client handler
# -------------------------------
    def handle_client(self, client_socket: socket.socket, addr: Tuple[str, int]) -> None:
        """
        Handle a single client connection.

        This function:
        - Parses the HTTP request
        - Extracts method, path, headers, and body
        - Sends an HTTP response
        - Closes the client socket

        Args:
            client_socket (socket.socket): Connected client socket.
            addr (tuple): Client (IP, port).

        Returns:
            None
        """
        try:
            client_socket.settimeout(self.response_timeout)
            request = client_socket.recv(self.buffer_size)
            if not request:
                return

            header_bytes, body_bytes = request.split(b"\r\n\r\n", 1)
            lines = header_bytes.decode("utf-8", errors="replace").splitlines()
            request_line = lines[0]

            try:
                method, path, version = request_line.split()
            except ValueError:
                self.send_response(client_socket, 400, "Bad Request")
                print(f"[{addr[0]}:{addr[1]}] Malformed request line")
                return

            headers = self.parse_headers(lines[1:])

            body = ""
            if "content-length" in headers:
                length = int(headers["content-length"])
                body = body_bytes[:length].decode("utf-8", errors="replace")

            print(f"[{addr[0]}:{addr[1]}] {method} {path}")

            headers = "\n".join(f"\t{k}: {v}" for k, v in headers.items())
            response_body = (
                f"Method: {method}\n"
                f"Path: {path}\n"
                f"Version: {version}\n"
                f"Headers: \n{headers}\n"
                f"Body: \n{body}"
            )

            self.send_response(client_socket, 200, response_body)

        except socket.timeout:
            print(f"[{addr[0]}:{addr[1]}] Connection timed out")
        except Exception as e:
            print(f"[{addr[0]}:{addr[1]}] Error handling client: {e}")
            self.send_response(client_socket, 500, "Internal Server Error")
        finally:
            client_socket.close()

    # -------------------------------
    # Server loop
    # -------------------------------
    def start(self) -> None:
        """
        Start the HTTP server and listen for incoming connections.

        The server accepts connections indefinitely and
        handles each client in a separate daemon thread.

        Returns:
            None
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(self.host, self.port)
            server_socket.listen()

            print(f"Server listening on {self.host}:{self.port}")
            print("Press Ctrl+C to stop the server.\n")

            while True:
                client_socket, addr = server_socket.accept()
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, addr),
                    daemon=True)
                thread.start()

if __name__ == "__main__":
    my_http_server = HttpServer()
    my_http_server.start()