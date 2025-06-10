from bs4 import BeautifulSoup
import requests
import csv

file = open("scraped.csv", "w")
writer = csv.writer(file)
writer.writerow(["QUOTES", "AUTHORS"])

page = requests.get("https://quotes.toscrape.com/")
soup = BeautifulSoup(page.text, "html.parser")

quotes = soup.findAll("span", attrs={"class":"text"})
authors = soup.findAll("small", attrs={"class":"author"})

for q,a in zip(quotes, authors):
    print(q.text, a.text)
    writer.writerow([q.text, a.text])
file.close()


# Same thing - different method
# quotes = soup.findAll("div", attrs={"class":"quote"})
# for q in quotes:
#     t = q.findAll("span", attrs={"class":"text"})
#     a = q.findAll("small", attrs={"class":"author"})
#     print(t[0].text, a[0].text)