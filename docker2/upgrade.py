# source/selenium_core/__init__.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options
import time, shutil
import re

class SeleniumController:
    def open_page(self, host):
        geckodriver_path = shutil.which("geckodriver")
        if not geckodriver_path:
            raise EnvironmentError("Geckodriver not found. Please install it or ensure it's in your PATH.")
        service = FirefoxService(executable_path=geckodriver_path)  # adjust path if needed
        self.driver = webdriver.Firefox(service=service)
        self.url = host
        self.driver.get(self.url)

    def open_page_chromium(self, host):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.url = host
        self.driver.get(self.url)

    def login_page(self,username,password):
        pass

    def readtext(self, **kwargs) -> str:
        """
        Read text from an element using a flexible locator.
        Usage:
            readtext(id="element_id")
            readtext(xpath="//div[@class='value']")
            readtext(class_name="value")
        """
        wait = WebDriverWait(self.driver, 10)
        if "id" in kwargs:
            element = wait.until(EC.presence_of_element_located((By.ID, kwargs["id"])))
        elif "xpath" in kwargs:
            element = wait.until(EC.presence_of_element_located((By.XPATH, kwargs["xpath"])))
        elif "class_name" in kwargs:
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, kwargs["class_name"])))
        else:
            raise ValueError("Please provide a valid locator: id, xpath, or class_name.")
        return element.text   
         
    def findtext_input(self, **kwargs):
        wait = WebDriverWait(self.driver, 10)
        if "id" in kwargs:
            keyword = kwargs["id"]
            self.input_element = wait.until(EC.presence_of_element_located((By.ID, keyword)))
        elif "xpath" in kwargs:
            keyword = kwargs["xpath"]
            self.input_element = wait.until(EC.presence_of_element_located((By.XPATH, keyword)))
        elif "class_name" in kwargs:
            keyword = kwargs["class_name"]
            self.input_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, keyword)))
        else:
            raise ValueError("Please provide a valid locator: id.")
        

    def sendtext(self, statement):
         self.input_element.send_keys(statement)

    def findbutton(self, **kwargs):
        """Find a clickable button by its locator and store it."""
        wait = WebDriverWait(self.driver, 10)
        if "id" in kwargs:
            self.button_element = wait.until(EC.element_to_be_clickable((By.ID, kwargs["id"])))
        elif "xpath" in kwargs:
            self.button_element = wait.until(EC.element_to_be_clickable((By.XPATH, kwargs["xpath"])))
        elif "class_name" in kwargs:
            self.button_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, kwargs["class_name"])))
        else:
            raise ValueError("Please provide a valid locator: id, xpath, or class_name.")
        # If no locator is provided, raise an error
        if not self.button_element:
            raise ValueError("Button not found. Please provide a valid locator: id, xpath, or class_name.")
        # If the button is not clickable, raise an error
        if not self.button_element.is_enabled():
            raise ValueError("Button is not clickable. Please check the locator or the button state.")
        # If the button is not visible, raise an error
        if not self.button_element.is_displayed():
            raise ValueError("Button is not visible. Please check the locator or the button state.")

    def sendbutton_click(self):
        """Click the previously found button."""
        self.button_element.click()

    def quit(self):
        """Gracefully shut down the browser."""
        self.driver.quit()

def extract_version(text):
    """Extract version number from a string."""
    match = re.search(r"\d+\.\d+\.\d+", text)
    if match:
        return match.group(0)
    return None

if __name__ == "__main__":

        # Example usage with Chromium
        controller = SeleniumController()
        controller.open_page_chromium("http://192.168.50.254:8888/")
        controller.findtext_input(id="firmware_name")
        time.sleep(1)  # Wait for the input field to be ready
        controller.sendtext("deneme1234.bin")
        time.sleep(2)
        controller.findbutton(xpath="//button[text()='OK']")
        controller.sendbutton_click()

        # time.sleep(5)  # Wait for a while to see the result
        # fw = controller.readtext(xpath='//*[@id="product-version"]/div[2]')
        # print(fw)  # Output: 23.10.6
        # version = extract_version(fw)
        # print(version)  # This will print only '23.10.6'
        # print("Title of the page is:", controller.driver.title)
        time.sleep(3)
        controller.quit()




