import logging
import time

from functools import wraps

def retry_decorator(timeout, retry_times: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            remaining_tries = retry_times

            while remaining_tries > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    logging.error(err)
                    last_exception = err
                    remaining_tries -= 1
                    if remaining_tries > 0:
                        logging.info('Retrying method call...')
                    time.sleep(timeout)
            raise last_exception
        return wrapper
    return decorator