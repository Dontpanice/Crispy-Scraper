from selenium import webdriver
from config import DRIVER_PATH

driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://google.com')
