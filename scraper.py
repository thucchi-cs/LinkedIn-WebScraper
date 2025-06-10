from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/company/comvest-partners/about/")
print(driver.current_url)

name = driver.find_element(By.TAG_NAME, "h1")
print(name.text)


# break-words white-space-pre-wrap t-black--light text-body-medium