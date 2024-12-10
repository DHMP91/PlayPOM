# PlayPOM
A library to enforce the page object design pattern with playwright. 


# Installation
To install the project add to requirement file:
````
git+https://github.com/DHMP91/PlayPOM.git
````
or
````
pip install git+https://github.com/DHMP91/PlayPOM.git
````


# Page Class
The default value of BASE_URL is `https://{host}:{port}` and to
instantiate a class it's as simple as:
```python
# PyTest Example
def test_sample(context, variables):
    page = context.new_page()
    BasePage(page, host="youtube.com").open() # Youtube landing page
```

However directly using BasePage is not the best practice. 
Instead, it is best to create a dedicated class for each page by inheriting `BasePage`:
```python
class GitHubPage(BasePage):
    URL_BASE = "https://github.com/"
    ...
```
```python  
# PyTest Example
def test_sample(context, variables):
    page = context.new_page()
    github_page = GitHubPage(page)
    github_page.open() # GitHub landing page
```
Now each time you want to start a github page, you no longer need to pass in the url.
This also makes it easier to change if the domain of the page changes in the future.


How about sub pages? You can create a partial URL and extend the main page
Here is an example of a user github page with the `USER_ID` passed in during instantiation:

```python
class GitHubUserPage(GitHubPage): # See above example for GitHubPage class
    URL_TEMPLATE = "/{USER_ID}"
    
    ...
```

```python
# PyTest Example
def test_partial_url(context, variables):
    page = context.new_page()
    GitHubUserPage(page, USER_ID="DHMP91").open() # Welcome to my github page!
```


# Region class and locators

A region represents a part of a page or a section within a page. By dividing a page into smaller sections (referred to as regions), it becomes easier to organize methods and locators for reuse across different page classes. In other words, a region can belong to multiple page classes. This approach is similar to how UI components are often reused within the same page.

Here is a region of the google page as an example, where the region is the search bar:
```python
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
```

All the locators for the region are defined in the constructor, making it easier to identify and update them when needed. 

The region class contains only the methods related to actions within the search bar.

The region class also includes two additional built-in functionalities:
- Automatic Wait: The region automatically waits to be fully loaded before executing further actions, as defined by the loaded function.
- Scoped Locator Search: Using self.in_region.get_by_title(...), the region restricts locator searches to within its scope (i.e., descendants of the root locator).
  This makes locators defined within the region more reliable and less susceptible to product changes.

In summary, in addition to page class, region class ensures better organization and maintainability.


# Inspiration
This approach is heavily inspired by PyPOM, originally created by the Mozilla team for Selenium/Splinter. However, since that project is no longer actively maintained and I needed a solution for Playwright, I decided to create one myself. I hope you find it useful!
