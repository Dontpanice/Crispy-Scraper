#!/usr/bin/env python
# coding: utf-8

# In[112]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm
from datetime import datetime


# In[113]:


def get_links(query: str) -> list:
    response = requests.get(f'https://www.gp.se/nyheter/västsverige?q={query}')
    soup = BeautifulSoup(response.content)
    # get the results count
    num_results = soup.find('p', class_=re.compile('c-search-results__title')).text
    num_results = [int(s) for s in num_results.split() if s.isdigit()][1]
    results_per_page = 10
    links = []
    dates = []
    for page in range(1, 2):#int(num_results/results_per_page) + 1):
        print ("Current page: " + str(page))
        url = f"https://www.gp.se/nyheter/sverige?q={query}&page={page}"
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        links += ["https://gp.se"+a.attrs.get('href') for
                  a in soup.find_all('a', class_=re.compile('c-teaser__link'))]
    return links


# In[114]:


def collect_data(source_page):
    
    PATTERN_HEADLINE_TEXT = re.compile(r"(?<=\"headline\">)[A-Öa-ö 0-9.!?,-s–]+(?=<\/h1>)")
    PATTERN_BROAD_TEXT = re.compile(r"(?<=fomaker.se\/idf\/1.0\">)[A-Öa-ö -0-9.!?,–]+(?=<\/element>)")
    PATTERN_LINK_TEXT = re.compile(r"(?<=\"c-article__body__content\">)[\nA-Öa-ö -0-9.!?,–<>=:0-9]+")
    ARTICLE_DATE = re.compile(r'(?<=datetime\=)[A-Öa-ö 0-9.!?,-:"]+(?=\sitemprop\=\"datePublished\">)')
    
    title = re.findall(PATTERN_HEADLINE_TEXT, source_page)
    date = datetime.fromisoformat(re.findall(ARTICLE_DATE, source_page)[0][1:-2])
    collected = []
    
    for match in re.finditer(PATTERN_LINK_TEXT, source_page):
        text = match.group() + " "
        span = match.span()
        data = (span, text)
        collected.append(data)

    if not collected:
        return "NULL","NULL","NULL"
    if not title:
        title = ["NULL"]
    if not date:
        date = ["NULL"]

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
        for text in BeautifulSoup(data[1]).find_all('p'):
            text_final += text.get_text()

    if not title:
        title = ["NULL"]

    return date, title[0], text_final


# In[115]:


def extract_content(links_list: list):
    contents = []
    for url in tqdm(links_list, desc="Loading..."):
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        date, title, text = collect_data(str(soup))
        contents.append({"date": date, "title": title, "article": text})
    return contents


# In[116]:


#links = get_links("mord")


# In[117]:


#extract_content([links[-1]])


# In[118]:


# Export as script
get_ipython().system('jupyter nbconvert --to script collect_data_from_links.ipynb')


# In[ ]:




