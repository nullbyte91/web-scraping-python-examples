from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import pandas as pd

# Chrome headless option to disable of opening browser every time
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors. 

driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=chrome_options)

products=[] #List to store name of the product
prices=[] #List to store price of the product
ratings=[] #List to store rating of the product

small_case_discover_uri = "https://smallcase.zerodha.com/discover/all?count=51"
small_case_base_uri = "https://smallcase.zerodha.com/smallcase/"
driver.get(small_case_discover_uri)

content = driver.page_source
soup = BeautifulSoup(content)
small_cases_id = []
for a in soup.findAll(attrs={'class':'DiscoverCard__sc-card___2YtVy'}):
    # Get all smallCase ID
    small_cases_id.append(a['id'])

for id, id_value in enumerate(small_cases_id):
    small_case_id_uri = small_case_base_uri + id_value
    print(small_case_id_uri)
    driver.get(small_case_id_uri)
    content = driver.page_source
    soup = BeautifulSoup(content)
    print(soup)
    exit(1)
    
# I am done, Just close the window
driver.close()
