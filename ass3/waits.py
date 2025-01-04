from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
import time

def setup_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver

def test_implicit_wait(driver):
    driver.get("https://demoqa.com/dynamic-properties")
    try:
        print("Testing: Implicit Wait")
        driver.implicitly_wait(15)  
        button = driver.find_element(By.ID, "visibleAfter")
        print("Button is visible:", button.is_displayed())
    except Exception as e:
        print("Error during implicit wait test:", e)
    finally:
        driver.implicitly_wait(10) 


def test_explicit_wait(driver):
    driver.get("https://demoqa.com/dynamic-properties")
    try:
        print("Testing: Explicit Wait")
        button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "enableAfter"))
        )
        print("Button is clickable:", button.is_enabled())
    except Exception as e:
        print("Error during explicit wait test:", e)



def test_fluent_wait(driver):
    driver.get("https://demoqa.com/dynamic-properties")
    try:
        print("Testing: Fluent Wait")
        fluent_wait = WebDriverWait(driver, 20, poll_frequency=1, 
                                     ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])

        button = fluent_wait.until(
            EC.element_to_be_clickable((By.ID, "enableAfter"))
        )
        print("Button is clickable after wait:", button.is_enabled())
    except Exception as e:
        print("Error during fluent wait test:", e)

def main():
    driver = setup_driver()
    try:
        test_implicit_wait(driver)
        test_explicit_wait(driver)
        test_fluent_wait(driver)
    finally:
        time.sleep(5)  
        driver.quit()

if __name__ == "__main__":
    main()
