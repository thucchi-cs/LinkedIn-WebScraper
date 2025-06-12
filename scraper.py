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
google = "https://www.linkedin.com/company/google"

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
    driver.get(url)

    # Get/display name of company
    name = driver.find_element(By.TAG_NAME, "h1")
    print(name.text)

    # Get headline of page
    try:
        headline = driver.find_element(By.CLASS_NAME, "top-card-layout__headline").text.strip()
    except:
        headline = ""
        print("no headline found")

    # Get quick info of page
    try:
        info = driver.find_element(By.CLASS_NAME, "line-clamp-2").text.strip()
    except:
        info = ""
        print("No quick info found")

    # Get about us section of page
    about = driver.find_elements(By.CLASS_NAME, "core-section-container")
    for a in about:
        if "about us" in a.text.lower():
            # Check for keywords
            for kw in keywords:
                if kw in a.text.strip().lower() + headline.lower() + info.lower():
                    print("keyword found")
                    break            
            else:
                print("no keywords")
                return False

    # Get followers count
    info2 = driver.find_element(By.CLASS_NAME, "top-card-layout__first-subline").text.split()
    followers = int(info2[-2].replace(",",""))
    # Check if followers count within range
    if 300 <= followers <= 15000:
        print("good followers")
    else:
        print("bad followers")
        return False

    # Get employees count
    info3 = driver.find_element(By.CLASS_NAME, "face-pile__text").text.split()
    employees = int(info3[-2].replace(",",""))
    # Check if employees count within range
    if 11 <= employees <= 200:
        print("good employees")
    else:
        print("bad employees")
        return False
    
    return True


# Check company's fit based on criteria
# print("\nFit criteria?", check_fit(google, driver))

sign_in(driver)
driver.get("https://www.linkedin.com/search/results/companies/")
print(driver.current_url)