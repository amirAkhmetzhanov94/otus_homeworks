import argparse
import os

from logger import logger


def parse_data(data: str):
    lines = data.split('\r\n')
    if not lines or not lines[0]:
        logger.warning("Empty request line")
        return
    method, path, http_version = lines[0].split()
    logger.info(f'Method: {method}, Path: {path}, HTTP Version: {http_version}')
    return method, path

def initiate_argument_parser():
    parser = argparse.ArgumentParser(
        prog='HTTP Server',
        description='OTUS Homework about HTTP server',
    )
    parser.add_argument('-r', '--doc-root')
    return parser

def read_template(
    root_path: str,
    requested_path: str,
):
    template_path = None
    template = None

    if '.ico' in requested_path:
        raise FileNotFoundError()

    template_path = f'{root_path}{requested_path}.html'

    if requested_path == '/':
        template_path = f'{root_path}/main.html'

    if os.path.exists(template_path):
        with open(template_path) as file:
            template = file.read()
        return template
    raise FileNotFoundError(f'File {template_path} could not be found')




