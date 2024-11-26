from __future__ import annotations
from types import MethodType
from playwright.sync_api import Page, TimeoutError
from playpom.decorators import generic_waiter, retrier

class PlaywrightPage(object):
    page: Page = None

    def __init__(self, page: Page):
        self.page = page

    def __getattr__(self, name):
        if hasattr(self.page, name):
            attr = getattr(self.page, name)
            if type(attr) == MethodType:
                return lambda *args, **kwargs: attr(*args, **kwargs)
            else:
                return attr

    @generic_waiter
    def wait_until(self, func, wait_time=30):
        if not callable(func):
            raise TypeError("parameter pass is not a callable function/method")
        return func()

    @retrier
    def retrier(self, func, wait_time=30, attempts=2):
        if not callable(func):
            raise TypeError("parameter pass is not a callable function/method")
        return func()

    def wait_until_loaded(self,  wait_time=30):
        if not callable(self.loaded):
            raise TypeError("loaded is not a callable function/method (Should not have @property).")
        if not self.wait_until(self.loaded,  wait_time=wait_time):
            raise TimeoutError("Page/Region did not load in time")
        return self

    def wait_for_page_to_load(self,  wait_time=30):
        self.wait_until_loaded(wait_time=wait_time)
        return self

    def wait_for_region_to_load(self,  wait_time=30):
        self.wait_until_loaded(wait_time=wait_time)
        return self
