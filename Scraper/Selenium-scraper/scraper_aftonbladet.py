from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_config import options, USERNAME, PASSWORD, PATTERN_BROAD_TEXT, PATTERN_LINK_TEXT
from config import DRIVER_PATH
from bs4 import BeautifulSoup
import time
import re
from scraper_functions import collect_data, scroll_to_bottom, driver_search, scroll_once, collect_page, collector, collect_elem_by_elem, collect_links
import pandas as pd

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.aftonbladet.se/sok")

# Do the search mord, göteborg
driver_search(driver, keywords="mord, göteborg", search_box_class_name="css-9rv3gz")
print("\n searching...")

links = collect_links(driver, element_class="css-3ks4jq")
print("finished")
df = pd.DataFrame()
df["links"] = links
df.to_csv("links.csv")


## TODO
# Automatically click the "okej" button on driver startup
# Fix collection of eleements when page is scrolling
# Refactor
