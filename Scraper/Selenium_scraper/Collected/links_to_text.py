from itertools import chain
import pandas as pd
from selenium import webdriver

from config import DRIVER_PATH
from Scraper.Selenium_scraper.scraper_functions import driver_search, collect_links, collect_liks_v2, collect_data
from Scraper.Selenium_scraper.selenium_config import options
import pandas as pd

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
links = pd.read_csv("links_mord, göteborg.csv")["link"]

for link in links:
    titles = []
    texts = []
    driver.get(link)
    source_page = driver.page_source
    title, text = collect_data(source_page)
    titles.append(title)
    texts.append(text)


df = pd.DataFrame()
df["titles"] = titles
df["texts"] = texts

df.to_csv("data.csv", sep=",")

# print(links)







# driver.get("https://www.aftonbladet.se/sok")
#
# # Do the search mord, göteborg
# driver_search(driver, keywords="mord, göteborg", search_box_class_name="css-9rv3gz")
# print("\n searching...")
#
# links = collect_links(driver, element_class="css-3ks4jq")
# print("finished")
# df = pd.DataFrame()
# df["links"] = links
# df.to_csv("links.csv")
