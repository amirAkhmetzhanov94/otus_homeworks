import logging
import argparse
import socket

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)


def initiate_argument_parser():
    parser = argparse.ArgumentParser(
        prog='HTTP Server',
        description='OTUS Homework about HTTP server',
    )
    parser.add_argument('-r', '--doc-root')
    return parser

def initiate_server_socket(
    address: str,
    port: int,
    number_of_clients: int,
):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((address, port))
    serversocket.listen(number_of_clients)
    return serversocket

def parse_data(
    data:str
):
    lines = data.split('\r\n')
    if not lines or not lines[0]:
        logger.warning("Empty request line")
        return
    method, path, http_version = lines[0].split()
    logger.info(f'Method: {method}, Path: {path}, HTTP Version: {http_version}')


def build_response():
    return (b'HTTP/1.1 200 OK\r\n'
            b'Content-Type: text/plain\r\n'
            b'Content-Length: 12\r\n'
            b'Connection: keep-alive\r\n\r\n'
            b'Hello World')


def main():
   parser = initiate_argument_parser()
   args = parser.parse_args()
   doc_root = args.doc_root
   if not doc_root:
       raise ValueError('Root folder must be set')
   logger.info(f'Document root is set to: {doc_root}')

   server_socket = initiate_server_socket('127.0.0.1', 8080, 5)

   while True:
       connection, address = server_socket.accept()
       logger.info(f'Connected by {address}')
       data = connection.recv(1024).decode('utf-8')

       if not data:
           connection.close()
           logger.info("Connection closed (no data)")
           continue

       parse_data(data)
       response = build_response()
       connection.sendall(response)
       connection.close()


if __name__ == '__main__':
    main()