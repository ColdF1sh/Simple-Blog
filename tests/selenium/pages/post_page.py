from selenium.webdriver.common.by import By

from .base_page import BasePage


class PostPage(BasePage):
    TITLE_INPUT = (By.ID, "id_title")
    CONTENT_INPUT = (By.ID, "id_content")
    POST_SUBMIT_BUTTON = (By.ID, "post-submit-button")
    POST_TITLE = (By.ID, "post-title")
    COMMENT_INPUT = (By.ID, "id_content")
    COMMENT_SUBMIT_BUTTON = (By.ID, "comment-submit-button")

    def create_post(self, title, content):
        self.type_text(*self.TITLE_INPUT, text=title)
        self.type_text(*self.CONTENT_INPUT, text=content)
        self.click(*self.POST_SUBMIT_BUTTON)

    def add_comment(self, comment_text):
        self.type_text(*self.COMMENT_INPUT, text=comment_text)
        self.click(*self.COMMENT_SUBMIT_BUTTON)

    def wait_for_post_title(self, title):
        self.wait_for_element(*self.POST_TITLE)
        self.wait_for_text(title)

    def wait_for_comment(self, comment_text):
        self.wait_for_text(comment_text)
