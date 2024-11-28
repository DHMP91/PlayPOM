from playpom.page import BasePage


class GitHubBasePage(BasePage):
    URL_BASE = "https://github.com/"


class GitHubUserPage(GitHubBasePage):
    URL_TEMPLATE = "/{USER_ID}"

    def loaded(self) -> bool:
        return True # not recommended, return true for sample. Please use proper locator(e.g locator(..).is_visible()
