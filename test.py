from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# driver = webdriver.Chrome()
# driver.get("https://github.com/login")
# print(driver.current_url)
# driver.find_element(By.NAME, "login").send_keys("thucchi-cs")
# driver.find_element(By.NAME, "password").send_keys("TraceyDo09")
# driver.find_element(By.NAME, "commit").click()
# print(driver.current_url)

r = range(201,500)
print(min(r), max(r))
print(min(r) >= 10 and max(r) <= 200)