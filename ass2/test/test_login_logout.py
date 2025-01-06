import unittest
from selenium import webdriver

import time
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
        error_message = self.login_page.get_error_message()
        self.assertTrue(error_message.is_displayed(), "Error message should be displayed for incorrect login")
        time.sleep(2)

    def test_login_success(self):
        """Test the login functionality with correct credentials."""
        self.login_page.login("standard_user", "secret_sauce")
        self.assertIn("inventory", self.driver.current_url, "Login failed, URL does not include 'inventory'")
        time.sleep(2)


    def test_logout(self):
        """Test the logout functionality."""
        self.login_page.login("standard_user", "secret_sauce")
        self.login_page.logout()
        self.assertIn("www.saucedemo.com", self.driver.current_url, "Did not return to login page after logout")
        time.sleep(2)


    def tearDown(self):
        """Tear down the webdriver."""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
