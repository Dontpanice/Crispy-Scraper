from selenium import webdriver
from config import DRIVER_PATH
from selenium_config import options, USERNAME, PASSWORD, PATTERN_BROAD_TEXT, PATTERN_LINK_TEXT
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re

from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.aftonbladet.se/sok")

time.sleep(1)
search = driver.find_element_by_class_name("css-9rv3gz")
time.sleep(1)
search.send_keys("mord, göteborg")
search.submit()
time.sleep(1)
search_results = driver.find_elements_by_class_name("css-1pslb2u")
# print(driver.page_source)
print("search_results", search_results)
wait = WebDriverWait(driver, 10)

for result in search_results:
    result.click()
    time.sleep(5)
    print("\n SOURCE -->", driver.page_source)

    # soup = BeautifulSoup(driver.page_source, features="html.parser")
    # text = soup.get_text()
    # print(text)

    collected = []
    for match in re.finditer(PATTERN_BROAD_TEXT, driver.page_source):
        text = match.group() + " "
        span = match.span()
        data = (span, text)
        collected.append(data)

    # Find span for broad text
    first_broad_span = collected[0][0][0]
    last_broad_span = collected[-1][0][1]

    # correct span for broad texts now when broadtext chunk span is found
    collected = [((n[0][0] - first_broad_span, n[0][1] - first_broad_span), n[1]) for n in collected]

    for match in re.finditer(PATTERN_LINK_TEXT, driver.page_source[first_broad_span:last_broad_span]):
        text = match.group() + " "
        span = match.span()
        data = (span, text)
        collected.append(data)

    collected.sort(key=lambda s: s[0])
    text_final = ""
    for data in collected:
        text_final += data[1]

    print(text_final)

    # print("\n URL --> ", driver.current_url)
    # title = driver.find_element_by_class_name("css-1oi9a7g").text
    # print("\n title --> ", title)
    # board_text_elements = driver.find_elements_by_class_name("css-10r2ygq")
    # print("\n board_text_elements --> ", board_text_elements)
    # board_text = [n.text for n in board_text_elements]
    # print("\n board_text --> ", title)

# button = driver.find_element_by_xpath("//button")
# button.click()
