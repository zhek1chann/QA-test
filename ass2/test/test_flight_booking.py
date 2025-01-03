import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By  # Ensure By is imported here
from pages.flight_booking_page import FlightBookingPage

class TestBlazeDemoFlightBooking(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.flight_booking_page = FlightBookingPage(self.driver)

    def test_flight_booking(self):
        self.flight_booking_page.book_flight("San Francisco", "London")
        self.flight_booking_page.fill_purchase_form()

        # Verify the confirmation message
        confirmation_message = self.driver.find_element(By.CSS_SELECTOR, "h1")
        self.assertTrue("Thank you for your purchase today!" in confirmation_message.text, "Confirmation message not displayed correctly")
        print("Flight booking was successful, and purchase confirmed.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
