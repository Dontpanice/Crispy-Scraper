from selenium_config import PATTERN_BROAD_TEXT, PATTERN_LINK_TEXT, PATTERN_HEADLINE_TEXT
import re
import time
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def collect_data(source_page):
    title = re.findall(PATTERN_HEADLINE_TEXT, source_page)

    collected = []
    for match in re.finditer(PATTERN_BROAD_TEXT, source_page):
        text = match.group() + " "
        span = match.span()
        data = (span, text)
        collected.append(data)

    if not collected:
        return ["NULL"], "NULL"

    # Find span for broad text
    first_broad_span = collected[0][0][0]
    last_broad_span = collected[-1][0][1]

    # correct span for broad texts now when broadtext chunk span is found
    collected = [((n[0][0] - first_broad_span, n[0][1] - first_broad_span), n[1]) for n in collected]

    for match in re.finditer(PATTERN_LINK_TEXT, source_page[first_broad_span:last_broad_span]):
        text = match.group() + " "
        span = match.span()
        data = (span, text)
        collected.append(data)

    collected.sort(key=lambda s: s[0])
    text_final = ""
    for data in collected:
        text_final += data[1]

    if not title:
        title = ["NULL"]

    return title[0], text_final


def scroll_to_bottom(driver):
    SCROLL_PAUSE_TIME = 3

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def scroll_once(driver, height=1080):
    driver.execute_script(f"window.scrollTo(0,{height} )")


def driver_search(driver, keywords="mord, göteborg", search_box_class_name="css-9rv3gz"):
    time.sleep(1)
    search = driver.find_element_by_class_name(search_box_class_name)
    time.sleep(1)
    search.send_keys(keywords)
    search.submit()
    time.sleep(1)


def collect_page(driver, page_nr="0", max_elements=1, class_name=None):
    titles = []
    texts = []
    for e in range(max_elements):
        search_elements = driver.find_elements_by_class_name(class_name)
        element_pick = search_elements[e]
        scroll_to_element(driver, element_pick)
        element_pick.click()
        time.sleep(5)
        # print("\n SOURCE -->", driver.page_source)
        title, text = collect_data(driver.page_source)
        titles.append(title)
        texts.append(text)
        df = pd.DataFrame()
        df["titles"] = titles
        df["texts"] = texts
        df.to_csv(f"./Collected/data_page{page_nr}.csv")

        driver.back()
        time.sleep(5)


def collector(driver, article_box="css-3ks4jq"):
    try:
        for page_nr in range(100):
            print("\n collecting...")
            search_elements = driver.find_elements_by_class_name(article_box)
            max_elements = len(search_elements)
            collect_page(driver, str(page_nr), max_elements)
            scroll_once(driver)
            print("\n scrolling...")
    except RuntimeError:
        print("Oops!  Something went wrong.  Try again...")


def collect_elem_by_elem(driver, element_class, n):
    try:
        titles = []
        texts = []
        df = pd.DataFrame()
        print("\n collecting...")
        t = time.time()
        elems = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, f".{element_class} [href]")))
        print("loaded in --> ", time.time() - t)
        articles_page_url = driver.current_url
        links = [elem.get_attribute('href') for elem in elems]
        last_elem = elems[-1]
        loc = last_elem.location
        size = last_elem.size
        # print("location of last element", last_elem.location)
        for link in links:
            driver.get(link)
            time.sleep(5)
            title, text = collect_data(driver.page_source)
            titles.append(title)
            texts.append(text)

        # save
        df["titles"] = titles
        df["texts"] = texts
        df.to_csv(f"./Collected/data{n}.csv")

        # return to page of articles
        driver.get(articles_page_url)

        # scroll to last read element
        print("\n Scrolling...")
        scroll_to_element(driver, loc, size)
        time.sleep(3)

        # Did we reach end of page?
        end_of_page = False
        return end_of_page

    except RuntimeError as e:
        print(e)


def collect_links(driver, element_class):
    try:
        links = []
        previous_links = []
        end_of_page = False
        while not end_of_page:
            print("\n collecting links")
            t = time.time()
            elems = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, f".{element_class} [href]")))
            print("loaded in --> ", time.time() - t)
            links_scroll = [elem.get_attribute('href') for elem in elems]
            if previous_links == links_scroll:
                end_of_page = True
            else:
                previous_links = links_scroll
            links.append(links_scroll)
            last_elem = elems[-1]
            loc = last_elem.location
            size = last_elem.size
            # scroll to last read element
            print("\n Scrolling...")
            scroll_to_element(driver, loc, size)
            time.sleep(3)

            # Did we reach end of page?
            # end_of_page = False
            print(len(links))

        return links

    except RuntimeError as e:
        print(e)


def scroll_to_element(driver, loc, size):
    # this scrolls until the element is in the middle of the page
    desired_y = (size['height']) + loc['y']
    current_y = (driver.execute_script('return window.innerHeight')) + driver.execute_script(
        'return window.pageYOffset')
    scroll_y_by = desired_y - current_y
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

# def scroll_to_element(driver, loc, size):
#     # this scrolls until the element is in the middle of the page
#     desired_y = (size['height'] / 2) + loc['y']
#     current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script(
#         'return window.pageYOffset')
#     scroll_y_by = desired_y - current_y
#     driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
