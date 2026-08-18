# Custom HTTP Server

A lightweight Python HTTP server that handles multiple clients simultaneously using sockets and threads. It supports basic HTTP requests (GET, POST, etc.) and prints the request method, path, headers, and body in the response.

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Limitations](#limitations)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## About the Project

This project is a small HTTP server built from scratch with Python's standard
`socket` and `threading` libraries. It is intended as a practical introduction
to the fundamentals of HTTP and network programming without relying on a web
framework.

The server listens for TCP connections on `127.0.0.1:8080`, processes each
client in a separate daemon thread, and parses the request line, headers, and
optional body. It then returns those values in a plain-text HTTP response,
making it easy to inspect how requests are received and handled.

The server parses the HTTP method and path, but it does not implement
route-specific behavior or serve application resources.

This is an educational implementation rather than a production-ready web
server. It focuses on the request/response flow and basic concurrency, with a
small buffer and a single request handled per connection.

## Features

- Handles multiple clients simultaneously using threads
- Parses HTTP method, path, version, headers, and body
- Returns a structured response including headers and body
- Supports small POST requests (body up to BUFFER_SIZE)

## Limitations

- Handles one request per connection
- Reads up to 1 KB from each client request
- Does not support chunked transfer encoding
- Does not support persistent connections

## Getting Started

### Prerequisites
Before getting started, ensure you have the following installed:
- [Python 3.8+](https://www.python.org/downloads/)

### Installation

1. **Clone the repository:**
```
git clone https://github.com/imseanconroy/custom-http-server.git
cd custom-http-server
```

2. **Create and activate the virtual environment:**
```
python3 -m venv env
source env/bin/activate
```

3. **Run the server:**
```
python3 server.py
```

4. **Default server settings:**
```
HOST: 127.0.0.1
PORT: 8080
```

*Press `Ctrl+C` in the terminal to stop the server.*

## Usage

GET Request
```bash
curl --location --request GET 'http://localhost:8080/hello-world' \
--header 'Content-Type: application/json'
```

POST Request
```bash
curl --location --request POST 'http://localhost:8080/hello-world' \
--header 'Content-Type: application/json' \
--data '{
    "message": "Hello, World!"
}'
```

Example server response:
```bash
Method: POST
Path: /hello-world
Version: HTTP/1.1
Headers:
	host: localhost:8080
	user-agent: curl/8.7.1
	accept: */*
	content-type: application/json
	content-length: 34
Body:
{
    "message": "Hello, World!"
}
```

## Contributing

Contributions are welcome. Please open an issue or fork the repository, create a new branch (`feature/your-feature-name`) and submit a pull request for any enhancements or bug fixes.

## License

This project is Distributed under the MIT License - see the [LICENSE](LICENSE) file for information.

## Support

If you are having problems, please let me know by [raising a new issue](https://github.com/ImSeanConroy/custom-http-server/issues/new/choose).
