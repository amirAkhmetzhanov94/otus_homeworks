import socket
import os

from abc import ABC
from collections.abc import Buffer

from logger import logger


class BaseServer(ABC):
    def initiate_server_socket(self):
        raise NotImplementedError

    def accept(self):
        raise NotImplementedError

    def serve(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def send(self, response: str):
        raise NotImplementedError



class BaseClient(ABC):
    def send(self, message: bytes):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError


class TCPServer(BaseServer):
    CONTENT_TYPE = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
    }

    def __init__(
        self,
        host: str,
        port: int,
        number_of_clients: int = None
    ):
        self.host = host
        self.port = port
        self.number_of_clients = number_of_clients
        self.server_socket = self.initiate_server_socket()
        self.connection = None

    def initiate_server_socket(
        self
    ):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(self.number_of_clients)
        return server_socket

    def close(self):
        self.server_socket.close()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def accept(self):
        return self.server_socket.accept()

    def serve(self):
        self.connection, address = self.accept()
        logger.info(f'Connected by {address}')
        data = self.connection.recv(1024).decode('utf-8')

        if not data:
            self.connection.close()
            logger.info("Connection closed (no data)")

        return data

    def send(self, response: Buffer):
        self.connection.sendall(response)

    def get_content_type(self, file_path: str):
        extension_name = os.path.splitext(file_path)[1].lower()
        return self.CONTENT_TYPE.get(extension_name, 'application/octet-stream')

    @staticmethod
    def build_response(
        message: str,
        status_code: int,
        content_length: int,
        content_type: str,
        status_message: str,
    ):
        return bytes(
            (
                f'HTTP/1.1 {status_code} {status_message}\r\n'
                f'Allow: GET, HEAD\r\n'
                f'Content-Type: {content_type}\r\n'
                f'Content-Length: {content_length}\r\n'
                f'Connection: keep-alive\r\n\r\n'
                f'{message}'
            ),
            encoding='utf-8'
        )


class TCPClient(BaseClient):
    def __init__(
        self,
        host: str,
        port: int,
    ):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.server_socket.connect((self.host, self.port))

    def send(self, message: bytes):
        self.server_socket.sendall(message)
