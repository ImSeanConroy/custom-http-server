# Custom HTTP Server

A lightweight Python HTTP server that handles multiple clients simultaneously using sockets and threads. It supports basic HTTP requests (GET, POST, etc.) and prints the request method, path, headers, and body in the response.

## Table of Contents

- [Getting Started](#getting-started)
- [Usage](#usage)
- [Features](#features)
- [License](#license)
- [Support](#support)

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

2. **Run the server:**
```
python server.py
```

3. **Default server settings:**
```
HOST: 127.0.0.1
PORT: 8080
```

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

## Features

- Handles multiple clients simultaneously using threads
- Parses HTTP method, path, version, headers, and body
- Returns a structured response including headers and body
- Supports small POST requests (body up to BUFFER_SIZE)

## License

This project is Distributed under the MIT License - see the [LICENSE](LICENSE) file for information.

## Support

If you are having problems, please let me know by [raising a new issue](https://github.com/ImSeanConroy/custom-http-server/issues/new/choose).
