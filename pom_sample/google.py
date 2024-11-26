from __future__ import annotations

from typing import List
from playwright.sync_api import Locator
from playpom.page  import BasePage
from playpom.region import BaseRegion


class Google(BasePage):
    URL_TEMPLATE = BasePage.URL_BASE

    def loaded(self) -> bool:
        return SearchRegion(self.page).root_locator.is_visible()

    def search_default(self, term):
        region = SearchRegion(self.page)
        region.search(term)
        region.click_google_search()

    def search_lucky(self, term):
        region = SearchRegion(self.page)
        region.search(term)
        region.click_im_feeling_lucky()


class SearchRegion(BaseRegion):
    def __init__(self, page):
        super(SearchRegion, self).__init__(page)
        self.root_locator = page.get_by_role("search")
        self.input_search_field = self.in_region.get_by_title("Search")
        self.google_search_buttons = self.in_region.get_by_label("Google Search")
        self.im_feeling_lucky_buttons = self.in_region.get_by_label("I'm Feeling Lucky")

    def loaded(self) -> bool:
        return self.root_locator.is_visible()

    def search(self, search_term):
        self.input_search_field.fill(search_term)

    def click_google_search(self):
        with self.page.expect_response(lambda response: "/complete/search?q=" in response.url):
            button = self.__get_visible_element(self.google_search_buttons.all())
            button.click()

    def click_im_feeling_lucky(self):
        with self.page.expect_response(lambda response: "/complete/search?q=" in response.url):
            button = self.__get_visible_element(self.im_feeling_lucky_buttons.all())
            button.click()

    @staticmethod
    def __get_visible_element(elements: List[Locator]):
        for element in elements:
            if element.is_visible():
                return element
        raise NoVisibleElementFound()


class NoVisibleElementFound(Exception):
    pass