import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


chromedriver = '/anaconda/bin/chromedriver'
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

driver.get("https://www.brewersassociation.org/directories/breweries/")
print(driver.title)
elem = driver.find_element_by_xpath('//*[@id="state"]')
print(elem)
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
driver.close()


