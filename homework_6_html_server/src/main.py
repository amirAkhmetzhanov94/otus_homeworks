import os

from logger import logger
from httpd import TCPServer
from utils import parse_data, initiate_argument_parser, read_template


def main():
   parser = initiate_argument_parser()
   args = parser.parse_args()
   doc_root = args.doc_root
   if not doc_root or not os.path.exists(doc_root):
       raise ValueError('Root folder must be set')
   logger.info(f'Document root is set to: {doc_root}')

   tcp_server = TCPServer('127.0.0.1', 8080, 5)

   while True:
       data = tcp_server.serve()
       if data is None:
           break
       method, path = parse_data(data)

       try:
           template = read_template(
               root_path=doc_root,
               requested_path=path
           )
       except FileNotFoundError:
           continue

       response = tcp_server.build_response(template, len(template))
       print(response)
       tcp_server.send(response)
       tcp_server.close_connection()

   tcp_server.close()

if __name__ == '__main__':
    main()