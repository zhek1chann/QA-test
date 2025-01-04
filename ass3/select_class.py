from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select  # Ensure this line is added
import time

def setup_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver


def test_select_class(driver):
    driver.get("https://demoqa.com/select-menu")
    try:
        print("Testing: Select Class")
        select_element = driver.find_element(By.ID, "oldSelectMenu")
        select = Select(select_element)
        select.select_by_value("3") 
        print("Selected option:", select.first_selected_option.text)
    except Exception as e:
        print("Error during select class test:", e)


def main():
    driver = setup_driver()
    try:
        test_select_class(driver)
    finally:
        time.sleep(5)  
        driver.quit()

if __name__ == "__main__":
    main()
