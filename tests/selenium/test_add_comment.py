import time

from tests.selenium.pages.home_page import HomePage
from tests.selenium.pages.login_page import LoginPage
from tests.selenium.pages.post_page import PostPage


USERNAME = "newuser"
PASSWORD = "simplepassword67"


def test_add_comment(driver, base_url):
    unique_suffix = int(time.time())
    title = f"Comment Target Post {unique_suffix}"
    content = "Post created before adding a comment."
    comment_text = f"Selenium comment {unique_suffix}"

    login_page = LoginPage(driver, base_url)
    home_page = HomePage(driver, base_url)
    post_page = PostPage(driver, base_url)

    login_page.open_home()
    login_page.go_to_login()
    login_page.login(USERNAME, PASSWORD)

    home_page.go_to_new_post()
    post_page.create_post(title, content)
    post_page.wait_for_post_title(title)
    post_page.add_comment(comment_text)
    post_page.wait_for_comment(comment_text)

    assert comment_text in driver.page_source
    post_page.take_screenshot("comment_added.png")
