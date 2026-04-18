from selenium.webdriver.common.by import By

from .base_page import BasePage


class LoginPage(BasePage):
    LOGIN_LINK = (By.ID, "nav-login-link")
    USERNAME_INPUT = (By.ID, "id_username")
    PASSWORD_INPUT = (By.ID, "id_password")
    SUBMIT_BUTTON = (By.ID, "login-submit-button")

    def open_home(self):
        self.open_url()

    def go_to_login(self):
        self.click(*self.LOGIN_LINK)

    def login(self, username, password):
        self.type_text(*self.USERNAME_INPUT, text=username)
        self.type_text(*self.PASSWORD_INPUT, text=password)
        self.click(*self.SUBMIT_BUTTON)
