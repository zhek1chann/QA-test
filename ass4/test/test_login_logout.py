import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException  
from pages.login_page import LoginPage

class TestSauceDemoLogin(unittest.TestCase):
    def setUp(self):
        """Setup the webdriver."""
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)


    def test_login_failure(self):
        """Test the login functionality with incorrect credentials."""
        self.login_page.login("standard_user", "wrong_password")
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-message-container.error")),
            "Error message not displayed for wrong password"
        )
        self.assertTrue(error_message.is_displayed(), "Error message should be displayed for incorrect login")

    def test_login_success(self):
        """Test the login functionality with correct credentials."""
        self.login_page.login("standard_user", "secret_sauce")
        self.assertIn("inventory", self.driver.current_url, "Login failed, URL does not include 'inventory'")


    def test_logout(self):
        """Test the logout functionality."""
        self.login_page.login("standard_user", "secret_sauce")

        # Open the menu to access the logout button
        menu_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "react-burger-menu-btn")),
            "Menu button not clickable or not found"
        )
        menu_button.click()

        # Now click the logout button
        logout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link")),
            "Logout button not clickable or not found"
        )
        logout_button.click()

        # Verify redirection to login page
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "login-button")),
            "Not redirected to login page after logout"
        )
        self.assertIn("www.saucedemo.com", self.driver.current_url, "Did not return to login page after logout")

    def tearDown(self):
        """Tear down the webdriver."""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
