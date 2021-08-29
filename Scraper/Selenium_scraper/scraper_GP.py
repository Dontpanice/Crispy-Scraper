from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import DRIVER_PATH
from selenium_config import options, USERNAME

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.gp.se/")

# login = driver.find_element_by_xpath("//input").send_keys(USERNAME)
driver.implicitly_wait(3)
login = driver.find_element_by_id("loginButton")
login.click()
# login.find_element_by_id('c1-login-field').send_keys(USERNAME)

loginname = driver.find_element_by_id('c1-login-field')
print(loginname)

loginname2 = driver.find_element_by_id('c1-login-form-group')
print(loginname2)

loginname = driver.find_element_by_name("login")
loginname.send_keys(USERNAME)

username_textbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "login")))

# loginname.click()

# print(loginname.text)
# loginname2 = driver.find_element_by_xpath('//*[@id="c1-login-field"]')

# print(loginname.text)
# print(loginname.)

# loginname.click()
# driver.implicitly_wait(3)
#
#
# # driver.find_element_by_id("c1-submit-button-form-group").click()
#
# loginname.send_keys(USERNAME)
# loginpass = driver.find_element_by_id("c1-password-field")
# loginpass.send_keys(PASSWORD)
# driver.implicitly_wait(2)
# login = driver.find_element_by_id("c1-submit-button-login")
# login.click()


# password = driver.find_element_by_xpath("//input[@type='password']").send_keys(PASSWORD)
# submit = driver.find_element_by_xpath("//input[@value='login']").click()
