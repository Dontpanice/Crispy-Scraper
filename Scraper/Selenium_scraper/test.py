import time

from selenium import webdriver

from config import DRIVER_PATH
from selenium_config import options


def scroll_to_element(driver, loc, size):
    # this scrolls until the element is in the middle of the page
    desired_y = (size['height'] / 2) + loc['y']
    current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script(
        'return window.pageYOffset')
    scroll_y_by = desired_y - current_y
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)


driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.aftonbladet.se/sok?q=mord%2C%20g%C3%B6teborg")

loc = {'x': 644, 'y': 2311}
size = {"height": 106}

time.sleep(3)
scroll_to_element(driver, loc, size)




