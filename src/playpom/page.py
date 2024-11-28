from __future__ import annotations
from urllib.parse import urlparse
from playwright.sync_api import Page

from playpom.exceptions import DefinePageClassURLException
from playpom.playwright_page import PlaywrightPage

class BasePage(PlaywrightPage):
    URL_TEMPLATE = None
    URL_BASE = "https://{host}:{port}"
    host = None
    port = None
    _url_kwargs = None
    _url = None

    def __init__(self, page: Page, timeout=30, **url_kwargs):
        page.set_default_timeout(timeout*1000)
        super(BasePage, self).__init__(page)
        if not self.URL_TEMPLATE and not self.URL_BASE:
            raise DefinePageClassURLException(
                "Please define a class variable 'URL_TEMPLATE' or 'URL_BASE' in the page class"
            )
        self._url_kwargs = url_kwargs

        if "port" not in self._url_kwargs:
            self._url_kwargs['port'] = 443

        if "host" not in url_kwargs.keys():
            parsed_url = urlparse(self.page.url)
            self.host = parsed_url.hostname
            self.port = parsed_url.port if parsed_url.port else self._url_kwargs['port']
        else:
            self.host = url_kwargs['host']
            self.port = url_kwargs['port']

    @property
    def url(self):
        if self._url:
            return self._url

        url = self.URL_BASE if self.URL_BASE else ""
        if self.URL_TEMPLATE:
            url = f"{url}/{self.URL_TEMPLATE}"
        formatted_url = url.format(**self._url_kwargs)
        self._url = formatted_url
        return url

    def loaded(self) -> bool:
        raise NotImplementedError("Please add a function loaded(self) -> bool to your Page Object Class")

    def open(self, loaded_check=True, wait_time=30):
        if loaded_check:
            self.page.wait_for_load_state("load")
            if hasattr(self, "loaded_context") and callable(self.loaded_context):
                with self.loaded_context():
                    self.page.goto(self.url)
            else:
                self.page.goto(self.url)
                self.wait_until_loaded(wait_time=wait_time)
        else:
            self.page.goto(self.url)
            self.page.wait_for_load_state("networkidle")
        return self