# Selenium notes



* driver.page_source - gets html page
* driver.title 
* driver.current_url
* driver.quit()


    # soup = BeautifulSoup(driver.page_source, features="html.parser")
    # text = soup.get_text()
    # print(text)


cur_win = driver.current_window_handle
driver.switch_to_window([win for win in driver.window_handles if win != cur_win[0]])

driver.close()
driver.switch_to_window(cur_win)