import pandas as pd
from selenium import webdriver

from config import DRIVER_PATH
from scraper_functions import driver_search, collect_links, collect_liks_v2
from selenium_config import options


SEARCH_TERM = "mord, göteborg"
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.aftonbladet.se/sok")

# Do the search mord, göteborg
driver_search(driver, keywords=SEARCH_TERM, search_box_class_name="css-9rv3gz")
print("\n searching...")

links = collect_liks_v2(driver, element_class="css-3ks4jq")
print("finished")
print(links)

df = pd.DataFrame()
df["link"] = links
df.to_csv(f"./Collected/links_{SEARCH_TERM}.csv", sep=",")



## TODO
# Automatically click the "okej" button on driver startup
# Fix collection of eleements when page is scrolling
# Refactor
