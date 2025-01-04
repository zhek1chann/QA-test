import unittest
from selenium import webdriver
from pages.search_page import SearchPage  # Make sure this import path is correct based on your project structure
import time

class TestSearchFunctionality(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.search_page = SearchPage(self.driver)

    def test_search(self):
        self.search_page.navigate_to_page()
        self.search_page.enter_search_term("Arcane")
        time.sleep(4)
        result_title = self.search_page.get_first_result_title()
        self.assertIn("Аркейн", result_title, "Selenium not found in the first result title")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
