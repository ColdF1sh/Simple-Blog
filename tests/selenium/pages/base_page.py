from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)
        self.screenshot_dir = Path(__file__).resolve().parent.parent / "screenshots"

    def open_url(self, path=""):
        self.driver.get(f"{self.base_url}{path}")

    def click(self, by, value):
        element = self.wait_for_element(by, value)
        element.click()

    def type_text(self, by, value, text):
        element = self.wait_for_element(by, value)
        element.clear()
        element.send_keys(text)

    def wait_for_element(self, by, value):
        return self.wait.until(ec.visibility_of_element_located((by, value)))

    def wait_for_text(self, text):
        self.wait.until(ec.presence_of_element_located((By.XPATH, f"//*[contains(., '{text}')]")))

    def take_screenshot(self, file_name):
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.driver.save_screenshot(str(self.screenshot_dir / file_name))
