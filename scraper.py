from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()
os.environ["HOME"] = "/tmp"

# Set up driver
def open_driver(user_data_dir):
    options = Options()
    print("good2")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.browser_version = 'stable'
    assert options.capabilities['browserVersion'] == 'stable'

    driver = webdriver.Chrome(options=options)
    return driver

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
def check_fit(url:str, driver:webdriver.Chrome, criteria:dict):
    results = {"Passed": True, "Error": None, "Keyword found": None, "Followers": None, "Employees": None}

    # Navigate to company's page
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)

    while "authwall" in driver.current_url:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(url)

    if (url != driver.current_url):
        print("could not access company", url, driver.current_url)
        results["Error"] = "Could not access company's LinkedIn."
        results["Passed"] = False
        return results

    # Get/display name of company
    try:
        name = driver.find_element(By.TAG_NAME, "h1")
        print(name.text)
    except:
        print("no name?")
        results["Error"] = "Could not access company's LinkedIn."
        results["Passed"] = False
        return results
    
    driver.save_screenshot("ss.png")

    if criteria["keywords"]:
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
        print(len(about), about[2].text)
        if len(about) < 1 and len(criteria["keywords"]) > 0:
            print("no about sections")
            results["Keyword found"] = False
            results["Passed"] = False
        
        for a in about:
            print(a.text.lower())
            if "about us" in a.text.lower():
                # Check for keywords
                for kw in criteria["keywords"]:
                    if kw in a.text.strip().lower() + headline.lower() + info.lower():
                        print("keyword found")
                        results["Keyword found"] = True
                        break            
                else:
                    results["Keyword found"] = False
                    results["Passed"] = False
                    print("no keywords")
                break
        else:
            if len(criteria["keywords"]) > 0:
                print("no about us")
                results["Keyword found"] = False
                results["Passed"] = False
        
    else:
        results["Keyword found"] = True

    # Get followers count
    try:
        info2 = driver.find_element(By.CLASS_NAME, "top-card-layout__first-subline").text.split()
        followers = int(info2[-2].replace(",",""))
        # Check if followers count within range
        if criteria["max_followers"] > 0:
            if criteria["min_followers"] <= followers <= criteria["max_followers"]:
                results["Followers"] = True
                print("good followers")
            else:
                results["Followers"] = False
                results["Passed"] = False
                print("bad followers")
        else:
            if criteria["min_followers"] <= followers:
                print("good followers")
                results["Followers"] = True
            else:
                results["Followers"] = False
                results["Passed"] = False
                print("bad followers")
    except:
        if criteria["min_followers"] != 0 or criteria['max_followers'] != 0:
            print("no followers")
            results["Followers"] = False
            results["Passed"] = False
    
    if criteria["min_followers"] == 0 and criteria["max_followers"] == 0:
        results["Followers"] = True

    # Get employees count
    try:
        info3 = driver.find_element(By.CLASS_NAME, "face-pile__text").text.split()
        employees = int(info3[-2].replace(",",""))
        # Check if employees count within range
        if criteria["max_employees"] > 0:
            if criteria["min_employees"] <= employees <= criteria["max_employees"]:
                print("good employees")
                results["Employees"] = True
            else:
                print("bad employees")
                results["Employees"] = False
                results["Passed"] = False
        else:
            if criteria["min_employees"] <= employees:
                print("good employees")
                results["Employees"] = True
            else:
                print("bad employees")
                results["Employees"] = False
                results["Passed"] = False
    except:
        if criteria['min_employees'] != 0 or criteria['max_employees'] != 0:
            print("no employees")
            results["Employees"] = False
            results["Passed"] = False

    if criteria["min_employees"] == 0 and criteria["max_employees"] == 0:
        results["Employees"] = True
    
    return results
