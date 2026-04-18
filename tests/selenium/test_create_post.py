import time

from tests.selenium.pages.home_page import HomePage
from tests.selenium.pages.login_page import LoginPage
from tests.selenium.pages.post_page import PostPage


USERNAME = "newuser"
PASSWORD = "simplepassword67"


def test_create_post(driver, base_url):
    unique_suffix = int(time.time())
    title = f"Selenium Post {unique_suffix}"
    content = "This post was created by Selenium WebDriver."

    login_page = LoginPage(driver, base_url)
    home_page = HomePage(driver, base_url)
    post_page = PostPage(driver, base_url)

    login_page.open_home()
    login_page.go_to_login()
    login_page.login(USERNAME, PASSWORD)

    home_page.go_to_new_post()
    post_page.create_post(title, content)
    post_page.wait_for_post_title(title)

    assert title in driver.page_source
    post_page.take_screenshot("post_created.png")
