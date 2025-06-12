from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

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

sign_in(driver)
driver.get("https://www.linkedin.com/search/results/companies/")
print(driver.current_url)
# print("\nFit criteria?", check_fit(comvest_partners, driver))