import os
import time
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


APP_URL = os.getenv("APP_URL", "http://web:5000")
SELENIUM_URL = os.getenv("SELENIUM_URL", "http://selenium:4444")


def wait_for_app(driver, timeout=60):
    end = time.time() + timeout
    while time.time() < end:
        try:
            driver.get(APP_URL)
            if "Student Notes App" in driver.page_source:
                return
        except Exception:
            pass
        time.sleep(2)
    raise RuntimeError("App did not become ready in time")


def create_driver_with_retry(options, timeout=90):
    end = time.time() + timeout
    last_error = None
    while time.time() < end:
        try:
            return webdriver.Remote(command_executor=SELENIUM_URL, options=options)
        except Exception as error:
            last_error = error
            time.sleep(2)
    raise RuntimeError(f"Selenium server did not become ready in time: {last_error}")


def run_test():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = create_driver_with_retry(options)
    wait = WebDriverWait(driver, 20)

    try:
        wait_for_app(driver)

        note_text = f"Note from selenium {int(time.time())}"
        note_input = wait.until(EC.presence_of_element_located((By.NAME, "note")))
        note_input.clear()
        note_input.send_keys(note_text)
        note_input.send_keys(Keys.ENTER)

        wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), note_text))
        print("Add note test passed")

        delete_links = driver.find_elements(By.LINK_TEXT, "Delete")
        if delete_links:
            delete_links[0].click()
            wait.until_not(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), note_text))
            print("Delete note test passed")
        else:
            raise AssertionError("Delete link not found")

    finally:
        driver.quit()


if __name__ == "__main__":
    try:
        run_test()
        print("Selenium tests completed successfully")
    except Exception as error:
        print(f"Selenium tests failed: {error}")
        sys.exit(1)
