from tests.selenium.pages.home_page import HomePage
from tests.selenium.pages.login_page import LoginPage


USERNAME = "newuser"
PASSWORD = "simplepassword67"


def test_login(driver, base_url):
    login_page = LoginPage(driver, base_url)
    home_page = HomePage(driver, base_url)

    login_page.open_home()
    login_page.go_to_login()
    login_page.login(USERNAME, PASSWORD)

    assert home_page.is_logged_in()
    home_page.take_screenshot("login_success.png")
