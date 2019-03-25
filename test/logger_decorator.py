# -*- coding: utf-8 -*-
from functools import wraps
import datetime
import time


def my_logger(original_function):
    import logging
    logging.basicConfig(filename='{}.log'.format(original_function.__name__), level=logging.INFO)

    @wraps(original_function)
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        logging.info(
            f'[{timestamp}] result: args - {args}, kwargs - {kwargs}')
        return original_function(*args, **kwargs)

    return wrapper


def my_timer(original_function):
    import time

    @wraps(original_function)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = original_function(*args, **kwargs)
        t2 = time.time() - t1
        print(f'{original_function.__name__} 함수 실행 시간: {t2}초')
        return result

    return wrapper


@my_timer
@my_logger
def display_info(name, age):
    time.sleep(1)
    print(f'display_info({name}, {age}) 함수가 실행되었습니다.')

display_info('John', 25)