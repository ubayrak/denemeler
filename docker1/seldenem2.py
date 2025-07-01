from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
driver.get("https://httpbin.org/html")
print(driver.title)
print(driver.find_element("tag name", "h1").text)
driver.quit()