from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
import time

def action_class_test_demoqa(driver):
    # Navigate to the Draggable page
    driver.get("https://demoqa.com/dragabble")
    print("1. Testing Draggable functionality")

    draggable = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "dragBox"))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", draggable)

    action = ActionChains(driver)
    offset_x = 50 
    offset_y = 50 
    action.drag_and_drop_by_offset(draggable, offset_x, offset_y).perform()
    time.sleep(2)


    # Navigate to the Droppable page
    print("2. Testing Droppable functionality")
    driver.get("https://demoqa.com/droppable")
    droppable_source = driver.find_element(By.ID, "draggable")
    droppable_target = driver.find_element(By.ID, "droppable")
    
    action.drag_and_drop(droppable_source, droppable_target).perform()
    time.sleep(2)
    print("3. Using SHIFT Key while typing")
    driver.get("https://demoqa.com/text-box")
    text_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "userName"))
    )

    action = ActionChains(driver)
    action.key_down(Keys.SHIFT).send_keys("hello").key_up(Keys.SHIFT).perform()
    print("Typed with SHIFT key: 'HELLO'")
    time.sleep(2)

    # Demonstrate CTRL+A and CTRL+C
    print("4. Perform CTRL+A and CTRL+C")
    action.click(text_input).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    time.sleep(1) 
    action.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
    print("Performed CTRL+A and CTRL+C: Text should be copied to clipboard")
    time.sleep(2)

    driver.quit()
   
    driver.quit()

def setup_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver

def main():
    driver = setup_driver()
    try:
        action_class_test_demoqa(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
