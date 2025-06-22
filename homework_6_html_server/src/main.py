import os

from logger import logger
from httpd import TCPServer
from utils import parse_data, initiate_argument_parser, read_template, define_template_path


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
       try:
           method, path = parse_data(data)

           if method not in ('GET', 'HEAD'):
               logger.error(f'{method} is not allowed')

               template_path = define_template_path(
                   doc_root,
                   requested_path='405'
               )
               template = read_template(template_path)
               response = tcp_server.build_response(
                   template,
                   status_code=405,
                   content_length=len(template),
                   content_type='text/html',
                   status_message='Not Allowed'
               )
               tcp_server.send(response)
               tcp_server.close_connection()
               continue

           template_path = define_template_path(doc_root, path)
           template = read_template(template_path)

           content_type = tcp_server.get_content_type(template_path)
           status_code = 200
           status_message = 'OK'

       except ValueError as err:
           logger.error(err)
           break

       except FileNotFoundError as err:
           logger.error(err)

           template_path = define_template_path(
               root_path=doc_root,
               requested_path='404'
           )
           template = read_template(template_path)

           content_type = 'text/html'
           status_code = 404
           status_message = 'Not Found'

       response = tcp_server.build_response(
           template,
           status_code,
           len(template),
           content_type,
           status_message,
       )

       tcp_server.send(response)
       tcp_server.close_connection()

   tcp_server.close()
   logger.info("Server closed")

if __name__ == '__main__':
    main()