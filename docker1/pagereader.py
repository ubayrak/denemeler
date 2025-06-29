from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def extract_version(text):
    match = re.search(r"\d+\.\d+\.\d+", text)
    if match:
        return match.group(0)
    return None

def main():
    url = "http://192.168.50.254:8888/"
    options = Options()
    options.headless = True  # Required for Docker

    # Start Firefox in headless mode
    driver = webdriver.Firefox(options=options)
    try:
        driver.get(url)
        # Wait for the element with id="product-version" to appear
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.ID, "product-version")))
        version = extract_version(element.text)
        if version:
            print(f"Found version: {version}")
        else:
            print("Version not found in element text.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()




