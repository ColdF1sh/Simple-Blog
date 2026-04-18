from selenium.webdriver.common.by import By

from .base_page import BasePage


class HomePage(BasePage):
    NEW_POST_LINK = (By.ID, "nav-new-post-link")
    PROFILE_LINK = (By.ID, "nav-profile-link")
    LOGOUT_BUTTON = (By.ID, "nav-logout-button")
    USER_GREETING = (By.ID, "nav-user-greeting")

    def open_home(self):
        self.open_url()

    def go_to_new_post(self):
        self.click(*self.NEW_POST_LINK)

    def open_profile(self):
        self.click(*self.PROFILE_LINK)

    def is_logged_in(self):
        self.wait_for_element(*self.LOGOUT_BUTTON)
        self.wait_for_element(*self.USER_GREETING)
        return True
