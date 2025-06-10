from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
keywords = ["private credit", "direct lending", "restructuring", "opportunistic credit", "special situations", "private debt", "structured credit", "reorganizations"]

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


# driver.get("https://www.linkedin.com/search/results/companies/?origin=SWITCH_SEARCH_VERTICAL&sid=WLb")

# Example companies' urls
comvest_partners = "https://www.linkedin.com/company/comvest-partners/"
monroe_capital = "https://www.linkedin.com/company/monroe-capital/"
google = "https://www.linkedin.com/company/google"
# Check company's fit based on criteria
# print("\nFit criteria?", check_fit(google, driver))


driver.get("https://www.linkedin.com/home")
sign_in = driver.find_element(By.CLASS_NAME, "nsm7Bb-HzV7m-LgbsSe-BPrWId")
print(sign_in.text)
sign_in.click()
current_window = None
for window in driver.window_handles:
    if window == driver.current_window_handle:
        current_window = window
    else:
        driver.switch_to.window(window)
print(driver.current_url)
email = driver.find_element(By.NAME, "identifier")
print(len(driver.find_elements(By.NAME, "Passwd")))
email.clear()
email.send_keys("dothucchi@gmail.com")

next_btn = driver.find_elements(By.TAG_NAME, "button")
next_btn = driver.find_element(By.CLASS_NAME, "VfPpkd-LgbsSe-OWXEXe-k8QpJ")
# print(len(next_btn))
next_btn.click()
# for btn in next_btn:
#     print("\"", btn.text, "\"")
#     if btn.text == "Next":
#         print(btn.text)
#         # btn.click()
#         btn.click()
print(driver.current_url)
print(len(driver.find_elements(By.NAME, "Passwd")))
