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
