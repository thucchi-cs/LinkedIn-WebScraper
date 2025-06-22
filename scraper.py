from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import time

# Load .env file
load_dotenv()

# Set up driver
driver = webdriver.Chrome()

# Keywords to find in a company
keywords = ["private credit", "direct lending", "restructuring", "opportunistic credit", "special situations", "private debt", "structured credit", "reorganizations"]

# Example companies' urls
comvest_partners = "https://www.linkedin.com/company/comvest-partners/"
monroe_capital = "https://www.linkedin.com/company/monroe-capital/"
google = "https://www.linkedin.com/company/google/"

# Scroll the page to set height
def scroll(driver:webdriver.Chrome, h:str="document.body.scrollHeight"):
    driver.execute_script(f"window.scrollTo(0,{str(h)})")
    print("scrolled", driver.execute_script("return window.scrollY"))

# Sign in to LinkedIn
def sign_in(driver:webdriver.Chrome):
    # Go to LinkedIn page
    driver.get("https://www.linkedin.com/home")

    # Click sign in
    sign_in = driver.find_element(By.CLASS_NAME, "sign-in-form__sign-in-cta")
    print(sign_in.text)
    sign_in.click()

    # Fill out sign in form and submit
    form = driver.find_element(By.CLASS_NAME, "login__form")
    form.find_element(By.ID, "username").send_keys(os.getenv("LINKEDIN_EMAIL"))
    form.find_element(By.ID, "password").send_keys(os.getenv("LINKEDIN_PWD"))
    form.submit()


# Check if company fits criteria given the linkedin page
def check_fit(url:str, driver:webdriver.Chrome):
    # Navigate to company's page
    driver.get(f"{url}about")

    # Get/display name of company
    name = driver.find_element(By.TAG_NAME, "h1")
    print(name.text)

    # Get headline of page
    try:
        tagline = driver.find_element(By.CLASS_NAME, "org-top-card-summary__tagline").text.strip()
    except:
        tagline = ""
        print("no tagline found")

    # Get about us section of page
    about = driver.find_element(By.CLASS_NAME, "org-page-details-module__card-spacing")
    # Check for keywords in about section and tagline
    for kw in keywords:
        if kw in about.text.strip().lower() + tagline.lower():
            print("keyword found")
            break            
    else:
        print("no keywords")
        return False

    # Quick summary of company
    summary = driver.find_element(By.CLASS_NAME, "org-top-card-summary-info-list").text.split()
    
    # Get followers count
    followers = summary[summary.index("followers") - 1]
    followers = followers.replace("K", "000")
    followers = followers.replace("M", "000000")
    followers = int(followers)
    # Check if followers count within range
    if 300 <= followers <= 15000:
        print("good followers")
    else:
        print("bad followers")
        return False

    # Get employees count
    employees = summary[summary.index("employees") - 1]
    if "+" in employees:
        print("bad employees")
        return False
    employees = employees.split("-")
    employees = range(int(employees[0]), int(employees[1])+1)
    # Check if employees count within range
    if (min(employees) >= 1) and (max(employees) <= 200):
        print("good employees")
    else:
        print("bad employees")
        return False
    
    return True


# Check company's fit based on criteria
# print(check_fit_logged_out(monroe_capital, driver))

sign_in(driver)
driver.get("https://www.linkedin.com/search/results/companies/")
past_url = driver.current_url
while past_url == driver.current_url:
    pass
urls = driver.current_url.split("?")
url = f"{urls[0]}?page=13&{urls[1]}"
driver.get(url)
time.sleep(5)
while True:
    while past_url == driver.current_url:
        pass
    print(driver.current_url)
    past_url = driver.current_url
    found = False
    companies = driver.find_elements(By.CLASS_NAME, "UNeRdMUvGhpkgiDasaJiuwbKqtfYq")
    for c in companies:
        name = c.find_element(By.CLASS_NAME, "IbXSFTBYTyznEViQKLhnyJdaNacpfgWZHYkE")
        if "comvest" in name.text.lower():
            print(name.text)
            print("this", driver.current_url)
            found = True
            break
    if found:
        break
    scroll(driver)
    time.sleep(1)
    next_btn = driver.find_element(By.CLASS_NAME, "artdeco-button--icon-right")
    if next_btn.is_enabled():
        next_btn.click()
        continue
    break



# # for i in range(2):
# time.sleep(5)
# companies = driver.find_elements(By.CLASS_NAME, "UNeRdMUvGhpkgiDasaJiuwbKqtfYq")
# # links = ["https://www.linkedin.com/company/amazon/", "https://www.linkedin.com/company/apple/"]
# links = []
# for c in companies:
#     name = c.find_element(By.CLASS_NAME, "IbXSFTBYTyznEViQKLhnyJdaNacpfgWZHYkE")
#     print(name.text)
#     links.append(name.get_attribute("href"))
#     # print(check_fit_logged_out(name.get_attribute("href"), check_driver))

# for l in links:
#     print(check_fit(l, driver))

# time.sleep(5)
# companies = driver.find_elements(By.CLASS_NAME, "UNeRdMUvGhpkgiDasaJiuwbKqtfYq")
# print(len(companies))
# for c in companies:
#     name = c.find_element(By.CLASS_NAME, "IbXSFTBYTyznEViQKLhnyJdaNacpfgWZHYkE")
#     print(name.text)
#     print(name.get_attribute("href"))

# for i in range(2):
#     time.sleep(5)
#     print(driver.current_url)
#     companies = driver.find_elements(By.CLASS_NAME, "UNeRdMUvGhpkgiDasaJiuwbKqtfYq")
#     print(len(companies))
#     for c in companies:
#         name = c.find_element(By.CLASS_NAME, "IbXSFTBYTyznEViQKLhnyJdaNacpfgWZHYkE")
#         print(name.text)
#     scroll(driver)
#     print("next elem #", len(driver.find_elements(By.CLASS_NAME, "artdeco-button--icon-right")))
#     next_btn = driver.find_element(By.CLASS_NAME, "artdeco-button--icon-right")
#     print(next_btn.text)
#     print(next_btn.is_enabled())
#     next_btn.click()
# print("out")
# url = driver.current_url
# print(url)
# url = url.replace("2", "100")
# driver.get(url)
# time.sleep(5)
# print(driver.current_url)
# companies = driver.find_elements(By.CLASS_NAME, "UNeRdMUvGhpkgiDasaJiuwbKqtfYq")
# print(len(companies))
# for c in companies:
#     name = c.find_element(By.CLASS_NAME, "IbXSFTBYTyznEViQKLhnyJdaNacpfgWZHYkE")
#     print(name.text)
# scroll(driver)
# print("next elem #", len(driver.find_elements(By.CLASS_NAME, "artdeco-button--icon-right")))
# next_btn = driver.find_element(By.CLASS_NAME, "artdeco-button--icon-right")
# print(next_btn.text)
# print(next_btn.is_enabled())
driver.close()
