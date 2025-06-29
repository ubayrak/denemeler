# source/selenium_core/__init__.py

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
import time, shutil

class SeleniumController:
    def open_page(self, host):
        geckodriver_path = shutil.which("geckodriver")
        if not geckodriver_path:
            raise EnvironmentError("Geckodriver not found. Please install it or ensure it's in your PATH.")
        options = Options()
        options.headless = True  # Always headless for Docker
        service = FirefoxService(executable_path=geckodriver_path)
        self.driver = webdriver.Firefox(service=service, options=options)
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
         
    
    def findtext_input(self, keyword):
         wait = WebDriverWait(self.driver, 10)
         self.input_element = wait.until(EC.presence_of_element_located((By.ID, keyword)))


    def sendtext(self, statement):
         self.input_element.send_keys(statement)


    def findbutton(self, xpath):
        """Find a clickable button by its XPath and store it."""
        wait = WebDriverWait(self.driver, 10)
        self.button_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))


    def sendbutton_click(self):
        """Click the previously found button."""
        self.button_element.click()


    def quit(self):
        """Gracefully shut down the browser."""
        self.driver.quit()

import re
def extract_version(text):
    """Extract version number from a string."""
    match = re.search(r"\d+\.\d+\.\d+", text)
    if match:
        return match.group(0)
    return None

    
if __name__ == "__main__":
        

        # Example usage
        controller = SeleniumController()
        controller.open_page("http://192.168.50.254:8888/")
        # controller.findtext_input("firmware_name")
        # time.sleep(1)  # Wait for the input field to be ready
        # controller.sendtext("deneme1234.bin")
        # time.sleep(2)
        # controller.findbutton("//button[text()='OK']")
        # controller.sendbutton_click()

        time.sleep(5)  # Wait for a while to see the result
        fw = controller.readtext(id="product-version")
        version = extract_version(fw)
        print(version)  # This will print only '23.10.6'
        time.sleep(2)
        controller.quit()


""" TOBE CONTINUED
def compare_versions(v1, v2):
    # Return 1 if v1 > v2, -1 if v1 < v2, 0 if equal.
    t1 = tuple(map(int, v1.split('.')))
    t2 = tuple(map(int, v2.split('.')))
    if t1 > t2:
        return 1
    elif t1 < t2:
        return -1
    else:
        return 0

# Example usage:
version1 = "23.10.6"
version2 = "24.5.2"
result = compare_versions(version1, version2)
if result == 1:
    print(f"{version1} is newer")
elif result == -1:
    print(f"{version2} is newer")
else:
    print("Versions are equal")"""




