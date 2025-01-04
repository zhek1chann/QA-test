# flight_booking_page.py
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage  # Assuming this class is properly defined in the base_page module

class FlightBookingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://blazedemo.com/")

    def select_city(self, dropdown_selector, city_name):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, dropdown_selector))
        )
        dropdown.click()
        dropdown.send_keys(city_name)
        dropdown.send_keys(Keys.ENTER)

    def book_flight(self, from_location, to_location):
        self.select_city("select[name='fromPort']", from_location)
        self.select_city("select[name='toPort']", to_location)
        search_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        search_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table"))
        )
        # Select the first available flight
        self.select_first_flight()

    def select_first_flight(self):
        first_flight_button = self.driver.find_element(By.CSS_SELECTOR, "table.table tbody tr:first-child td input")
        first_flight_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2"))
        )

    def fill_purchase_form(self):
        self.driver.find_element(By.ID, "inputName").send_keys("John Doe")
        self.driver.find_element(By.ID, "address").send_keys("123 Main St.")
        self.driver.find_element(By.ID, "city").send_keys("Anytown")
        self.driver.find_element(By.ID, "state").send_keys("State")
        self.driver.find_element(By.ID, "zipCode").send_keys("12345")
        self.driver.find_element(By.ID, "cardType").send_keys("Visa")
        self.driver.find_element(By.ID, "creditCardNumber").send_keys("4111111111111111")
        card_month = self.driver.find_element(By.ID, "creditCardMonth")
        card_month.clear()
        card_month.send_keys("12")
        card_year = self.driver.find_element(By.ID, "creditCardYear")
        card_year.clear()
        card_year.send_keys("2025")
        self.driver.find_element(By.ID, "nameOnCard").send_keys("John Doe")
        self.driver.find_element(By.ID, "rememberMe").click()
        purchase_button = self.driver.find_element(By.CSS_SELECTOR, "input.btn-primary")
        purchase_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "h1"), "Thank you for your purchase today!")
        )
