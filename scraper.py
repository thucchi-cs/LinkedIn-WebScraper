from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Set up driver
def open_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headeless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Keywords to find in a company
keywords = ["private credit", "direct lending", "restructuring", "opportunistic credit", "special situations", "private debt", "structured credit", "reorganizations"]

# Scroll the page to set height
def scroll(driver:webdriver.Chrome, h:str="document.body.scrollHeight"):
    print("real scroll", driver.execute_script(f"return {h};"))
    driver.execute_script(f"window.scrollTo(0,{str(h)})")
    print("scrolled", driver.execute_script("return window.scrollY"))

# Sign in to LinkedIn
def sign_in(driver:webdriver.Chrome):
    # Go to LinkedIn page
    driver.get("https://www.linkedin.com/login")

    # Fill out sign in form and submit
    form = driver.find_element(By.CLASS_NAME, "login__form")
    form.find_element(By.ID, "username").send_keys(os.getenv("LINKEDIN_EMAIL"))
    form.find_element(By.ID, "password").send_keys(os.getenv("LINKEDIN_PWD"))
    form.submit()

# Check if company fits criteria given the linkedin page
def check_fit(url:str, driver:webdriver.Chrome):
    # Navigate to company's page
    driver.get(url)

    if (url != driver.current_url):
        print("could not access company")
        return False

    # Get/display name of company
    try:
        name = driver.find_element(By.TAG_NAME, "h1")
        print(name.text)
    except:
        print("no name?")
        return False

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
    if len(about) < 1:
        print("no about sections")
        return False
    
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
            break
    else:
        print("no about us")
        return False

    # Get followers count
    try:
        info2 = driver.find_element(By.CLASS_NAME, "top-card-layout__first-subline").text.split()
        followers = int(info2[-2].replace(",",""))
        # Check if followers count within range
        if 300 <= followers <= 15000:
            print("good followers")
        else:
            print("bad followers")
            return False
    except:
        print("no followers")
        return False

    # Get employees count
    try:
        info3 = driver.find_element(By.CLASS_NAME, "face-pile__text").text.split()
        employees = int(info3[-2].replace(",",""))
        # Check if employees count within range
        if 11 <= employees <= 200:
            print("good employees")
        else:
            print("bad employees")
            return False
    except:
        print("no employees")
        return False
    
    return True
