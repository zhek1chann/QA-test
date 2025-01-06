from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from .base_page import BasePage

class LoginPage():
    USERNAME_INPUT = (By.ID, 'user-name')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')
    MENU_BUTTON =  (By.ID, 'react-burger-menu-btn')
    LOGOUT_BUTTON =  (By.ID, 'logout_sidebar_link')
    def __init__(self, driver):
        self.driver = driver
        self.driver.get("https://www.saucedemo.com")

    def find_element(self, locator):
        return WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located(locator)
       )


    def enter_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_error_message(self):
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-message-container.error")),
            "Error message not displayed for wrong password"
        )
        return error_message

    def click(self, locator):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator)
        ).click()

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_BUTTON)

    def login(self, username, password):
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
    

