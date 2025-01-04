from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://hdrezka.ag/series/best/'
        self.search_box_locator = (By.ID, "search-field")
        self.first_result_title_locator = (By.ID, "search-results")

    def navigate_to_page(self):
        self.driver.get(self.url)

    def enter_search_term(self, search_term):
        search_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.search_box_locator)
        )
        search_box.send_keys(search_term)
        search_box.submit()

    def get_first_result_title(self):
        try:
            result_container = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".b-content__inline_item-link"))
            )
            result_title = result_container.find_element(By.CSS_SELECTOR, "a").text
            return result_title
        except TimeoutException:
            print("First result title not found or page did not load in time")
            return None
