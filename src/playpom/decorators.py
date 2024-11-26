from __future__ import annotations

import functools
import inspect
import logging
import time
from typing import Callable


log = logging.getLogger('netgovern')


def generic_waiter(func: Callable[..., bool]):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        params = inspect.signature(func).parameters
        wait_time = 10
        if 'wait_time' in params and params['wait_time'].default is not inspect.Parameter.empty:
            wait_time = params['wait_time'].default
        if 'wait_time' in kwargs:
            wait_time = kwargs.pop('wait_time')
        end_time = time.time() + wait_time
        while time.time() < end_time:
            try:
                if func(*args, **kwargs):
                    return True
            except NotImplementedError as e:
                raise e
            except:
                pass
        return False
    return wrapper_decorator


def format_locator(locator: str, **substitutions: str) -> str:
    """Format locator based on provided key arguments"""
    if substitutions:
        locator = locator.format(**substitutions)
    log.debug(f'Using locator: {locator}')
    return locator


def retrier(func: Callable):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        params = inspect.signature(func).parameters
        attempt = 0
        max_attempts = 5
        wait_time = None
        if 'wait_time' in params and params['wait_time'].default is not inspect.Parameter.empty:
            wait_time = params['wait_time'].default
        if 'wait_time' in kwargs:
            wait_time = kwargs.pop('wait_time')

        if 'attempts' in params and params['attempts'].default is not inspect.Parameter.empty:
            max_attempts = params['attempts'].default
        if 'attempts' in kwargs:
            max_attempts = kwargs.pop('attempts')

        while attempt <= max_attempts:
            attempt += 1
            try:
                value = func(*args, **kwargs)
                return value
            except Exception as exc:  # pylint: disable=broad-except
                if wait_time:
                    time.sleep(wait_time)
                if attempt == max_attempts:
                    raise exc
    return wrapper_decorator
