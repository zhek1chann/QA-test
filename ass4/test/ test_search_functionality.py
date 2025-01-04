from selenium import webdriver
from pages.search_page import SearchPage
import unittest

class TestSearchFunctionality(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.search_page = SearchPage(self.driver)

    def test_search(self):
        self.search_page.navigate_to_page()
        self.search_page.enter_search_term("Selenium")
        assert "Selenium" in self.search_page.get_first_result_title()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
