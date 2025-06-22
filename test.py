from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv

# Set up driver
driver = webdriver.Chrome()

# Keywords to find in a company
keywords = ["private credit", "direct lending", "restructuring", "opportunistic credit", "special situations", "private debt", "structured credit", "reorganizations"]

def check_fit(url:str, driver:webdriver.Chrome):
    # Navigate to company's page
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)

    # Get/display name of company
    try:
        name = driver.find_element(By.TAG_NAME, "h1")
        print(name.text)
        if "error" in name.text.lower():
            print("Error")
            driver.save_screenshot("ss.png")
            time.sleep(5)
            new = check_fit(url, driver)
            driver.close()
            return new
    except:
        print("no name?")
        driver.close()
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
        driver.close()
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
                driver.close()
                return False
            break
    else:
        print("no about us")
        driver.close()
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
            driver.close()
            return False
    except:
        print("no followers")
        driver.close()
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
            driver.close()
            return False
    except:
        print("no employees")
        driver.close()
        return False
    
    driver.close()
    return True

# print(check_fit("https://www.linkedin.com/company/capital-group", driver))

file = open("scraped.csv", "w")
writer = csv.writer(file)
writer.writerow(["Name", "Link"])

driver.get(f"https://www.linkedin.com/directory/companies/c-167")
counter = 0
while "https://www.linkedin.com/directory/companies/" not in driver.current_url:
    driver.execute_script("window.open('');")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.get(f"https://www.linkedin.com/directory/companies/c-167")
    time.sleep(1)
    counter += 1
    if counter > 10:
        break
companies = driver.find_elements(By.CLASS_NAME, "listings__entry-link")
good = []
directory_win = driver.current_window_handle
for c in companies[500:]:
    link = c.get_attribute("href")
    if check_fit(link, driver):
        name = c.text
        good.append(name)
        writer.writerow([name,link])
    time.sleep(0.5)
    driver.switch_to.window(directory_win)

file.close()