## Into to Client-Side Testing
Mark Lavin - DjangoCon 2015

@@

## WHOAMI

![Mark Lavin](./img/mark.jpg) <!-- .element: style="float: left" -->

- Technical Director at [Caktus Group](https://www.caktusgroup.com/)
- Co-Author of ["Lightweight Django"](http://shop.oreilly.com/product/0636920032502.do)
- [DrOhYes](https://twitter.com/DrOhYes) on Twitter
- [mlavin](https://github.com/mlavin) on Github

@@

## Goals

Notes:

Get you started testing with a pratical starting point.
This isn't an in-depth review of all testing tools.
Also not going to try to convince you to do testing.
I don't think that argument needs to be made anymore.

@@

## Outline

- Example Project
- Integration Tests with Selenium
- Unittests with Qunit

@@

## What Are We Testing

Demo: http://fileapi.mlavin.org/

Source: https://github.com/mlavin/fileapi

<insert screenshot of finished project>

Notes:
This is a minimal REST API (using JWT for auth) which allows drag and drop file uploads.
On the front-end it uses Backbone.

@@

## API Structure

```
    / - GET to render the app.
    /api-token/ - POST to exchange username/password for JWT.
    /uploads/ - GET to list all current uploads.
                POST to add a new file upload.
    /uploads/<name>/ - GET to see file details.
                       DELETE to remove the upload.
```

Notes:
No PUT for updating files once they've been uploaded.
You are welcome to review the view code but that isn't really the focus here.

@@

## Users Don't Care About Any of This

Notes:
User's don't care about your fancy pure-REST server implementation. They want
to do things: login to the site, navigate around, submit data, etc.

@@

## Testing What Users Do

Notes:
This is what Selenium is good at. It drives a web browser. You can interact with the DOM,
filling out forms, clicking links, etc.

@@

## Selenium Setup

```python
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

class FunctionalTests(StaticLiveServerTestCase):
    """Iteractive tests with selenium."""

    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.PhantomJS()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()
```

Notes:
The browser setup/teardown can be slow so it helps to only do it once per class. This doesn't
give perfect test isolation but it works well for most use cases.

I like PhantomJS which is a headless Webkit browser but you could replace this with the
Firefox, Chrome, or IE driver. PhantomJS is installed by default on TravisCI which is nice.


## First Selenium Test

```python
class FunctionalTests(StaticLiveServerTestCase):
    ...
    def test_show_login(self):
        """The login should be shown on page load."""

        self.browser.get(self.live_server_url)
        form = self.browser.find_element_by_id('login')
        upload = self.browser.find_element_by_id('upload')
        self.assertTrue(
            form.is_displayed(),
            'Login form should be visible.')
        self.assertFalse(
            upload.is_displayed(),
            'Upload area should not be visible.')

```

Notes:
This is the first taste of what you can do with Selenium. Find elements in the DOM and assert
things about them. In this case a user expects to load the app and see the login form.


## Form Submission

```python
class FunctionalTests(StaticLiveServerTestCase):
    ...
    def login(self, username, password):
        """Helper for login form submission."""

        self.browser.get(self.live_server_url)
        form = self.browser.find_element_by_id('login')
        username_input = form.find_element_by_name('username')
        username_input.send_keys(username)
        password_input = form.find_element_by_name('password')
        password_input.send_keys(password)
        form.submit()
```

Notes:
You can fill out forms by using ``send_keys`` once you have selected that element from the DOM.
You can submit a form by calling submit on the form itself (which would be like hitting enter)
or you could select submit button if there is one and submit it.


## Waiting

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
...
class FunctionalTests(StaticLiveServerTestCase):
    ...
    def test_login(self):
        """Submit the login form with a valid login."""

        self.login(self.username, self.password)
        WebDriverWait(self.browser, 5).until(
            expected_conditions.visibility_of_element_located(
                (By.ID, 'upload')))
        form = self.browser.find_element_by_id('login')
        self.assertFalse(
            form.is_displayed(),
            'Login form should no longer be visible.')
```

Notes:
WebDriverWait defines the API for explicit wait conditions. You can wait on a number
of different things such as existance of a new element or an JS alert or the page title
changing. In this case we wait for an element to become visible up to 5 seconds.

There are also implicit waits which will just wait for a set amount of time. Obviously that
will add time to your test runtime. And following the Zen of Python, explicit is better than
implicit.


## Users Aren't Always Right

```python
class FunctionalTests(StaticLiveServerTestCase):
    ...
    def test_invalid_login(self):
        """Submit the login form with an invalid login."""

        self.login(self.username, self.password[1:])
        error = WebDriverWait(self.browser, 5).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, 'error')))
        self.assertEqual('Invalid username/password', error.text)
        form = self.browser.find_element_by_id('login')
        self.assertTrue(
            form.is_displayed(),
            'Login form should still be visible.')
```

Note:
We want to test the things that users do and sometimes they make mistakes. You
should test those as well.

@@

## Resources

- https://docs.djangoproject.com/en/1.8/topics/testing/
- https://selenium-python.readthedocs.org/
- https://qunitjs.com/

@@

## Thanks!

### Questions?

http://talks.caktusgroup.com/djangocon/2015/client-side-testing/

*Book signing at the Caktus booth 2:50 PM*
