from __future__ import annotations

import abc
from typing import Optional, Union, Pattern

from playwright.sync_api import Locator, Page

from playpom.decorators import generic_waiter
from playpom.playwright_page import PlaywrightPage


class PostInitCaller(type):
    def __call__(cls, *args, **kwargs):
        """Called after __init__"""
        # print(f"{__class__.__name__}.__call__({args}, {kwargs})")
        obj = type.__call__(cls, *args, **kwargs)
        PostInitCaller._loaded(obj)
        return obj

    @staticmethod
    @generic_waiter
    def _loaded(obj):
        return obj.loaded


class MetaRegion(PostInitCaller, abc.ABCMeta):
    pass


class BaseRegion(PlaywrightPage):
    root_locator: Locator = None
    _region_locator: _RegionLocators = None

    def __init__(self, page: Page, root_locator: Locator = None, timeout=30):
        page.set_default_timeout(timeout*1000)
        super(BaseRegion, self).__init__(page)
        if root_locator:
            self.root_locator = root_locator
        self._region_locator = _RegionLocators(self)

    def loaded(self) -> bool:
        raise NotImplementedError("Please add a function loaded(self) -> bool to your Region Object Class")

    @property
    def in_region(self) -> _RegionLocators:
        return self._region_locator



class _RegionLocators(PlaywrightPage):
    region = None
    page = Page

    def __init__(self, region: BaseRegion):
        super().__init__(region.page)
        self.region = region

    @property
    def root_locator(self):
        return self.region.page if self.region.root_locator is None else self.region.root_locator

    def locator(
        self,
        selector: str,
        *,
        has_text: Optional[Union[str, Pattern[str]]] = None,
        has: Optional[Locator] = None
    ) -> Locator:
        return self.root_locator.locator(selector, has_text=has_text, has=has)

    def get_by_alt_text(
            self,
            text: Union[str, Pattern[str]],
            *,
            exact: Optional[bool] = None
    ) -> Locator:
        return self.root_locator.get_by_alt_text(text, exact=exact)

    def get_by_label(
            self,
            text: Union[str, Pattern[str]],
            *,
            exact: Optional[bool] = None
    ) -> Locator:
        return self.root_locator.get_by_label(text, exact=exact)

    def get_by_placeholder(
        self,
        text: Union[str, Pattern[str]],
        *,
        exact: Optional[bool] = None
    ) -> Locator:
        return self.root_locator.get_by_placeholder(text, exact=exact)

    def get_by_role(
        self,
        role,
        *,
        checked: Optional[bool] = None,
        disabled: Optional[bool] = None,
        expanded: Optional[bool] = None,
        include_hidden: Optional[bool] = None,
        level: Optional[int] = None,
        name: Optional[Union[str, Pattern[str]]] = None,
        pressed: Optional[bool] = None,
        selected: Optional[bool] = None,
        exact: Optional[bool] = None
    ) -> Locator:
        return self.root_locator.get_by_role(
                role=role,
                checked=checked,
                disabled=disabled,
                expanded=expanded,
                include_hidden=include_hidden,
                level=level,
                name=name,
                pressed=pressed,
                selected=selected,
                exact=exact
        )

    def get_by_test_id(self, test_id: Union[str, Pattern[str]]) -> Locator:
        return self.root_locator.get_by_test_id(test_id)

    def get_by_text(
            self,
            text: Union[str, Pattern[str]],
            *,
            exact: Optional[bool] = None
    ) -> Locator:
        return self.root_locator.get_by_text(text, exact=exact)

    def get_by_title(
            self,
            text: Union[str, Pattern[str]],
            *,
            exact: Optional[bool] = None
    ) -> Locator:
        return self.root_locator.get_by_title(text, exact=exact)
