import re
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = False  # Set to False if you want to see graphical interface
options.add_argument("--window-size=1920,1200")

# login information
USERNAME = "arnaud.jean.moulis@gmail.com"
PASSWORD = "illusive348"

# regex for finding text in html source page

PATTERN_HEADLINE_TEXT = re.compile(r"(?<=\"headline\">)[A-Öa-ö 0-9.!?,-]+(?=<\/h1>)")
PATTERN_BROAD_TEXT = re.compile(r"(?<=css-10r2ygq\">)[A-Öa-ö 0-9.!?,-]+(?=<)")
PATTERN_LINK_TEXT = re.compile(r"(?<=>)[A-Öa-ö 0-9.!?,-]+(?=<\/a>)")
