from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
# driver.get("https://www.linkedin.com/company/comvest-partners/")
driver.get("https://www.linkedin.com/company/monroe-capital/")
# driver.get("https://www.linkedin.com/company/google")
# print(driver.current_url)

fit = True
keywords = ["private credit", "direct lending", "restructuring", "opportunistic credit", "special situations", "private debt", "structured credit", "reorganizations", "financial services"]

name = driver.find_element(By.TAG_NAME, "h1")
print(name.text)

try:
    headline = driver.find_element(By.CLASS_NAME, "top-card-layout__headline").text.strip()
except:
    headline = ""
    print("no headline found")
# print(headline.text)

try:
    info = driver.find_element(By.CLASS_NAME, "line-clamp-2").text.strip()
except:
    info = ""
    print("No quick info found")
# print(info.text)

about = driver.find_elements(By.CLASS_NAME, "core-section-container")
for a in about:
    if "about us" in a.text.lower():
        # print(a.text)
        for kw in keywords:
            if kw in a.text.strip().lower() + headline.lower() + info.lower():
                print("keyword found")
                break            
        else:
            print("no keywords")
            fit = False

info2 = driver.find_element(By.CLASS_NAME, "top-card-layout__first-subline").text.split()
# print(info2.text)
followers = int(info2[-2].replace(",",""))
if 300 <= followers <= 15000:
    print("good followers")
else:
    print("bad followers")
    fit = False

info3 = driver.find_element(By.CLASS_NAME, "face-pile__text").text.split()
employees = int(info3[-2].replace(",",""))
if 11 <= employees <= 200:
    print("good employees")
else:
    print("bad employees")
    fit = False

print("\nFit criteria?", fit)

# break-words white-space-pre-wrap t-black--light text-body-medium
driver.get("https://www.linkedin.com/search/results/companies/?origin=SWITCH_SEARCH_VERTICAL&sid=WLb")