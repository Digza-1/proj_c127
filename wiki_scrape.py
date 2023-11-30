from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service


# wiki URL
START_URL = (
    "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
)
service = Service(executable_path="chromedriver-win64\\chromedriver.exe")
options = webdriver.ChromeOptions()

browser = webdriver.Chrome(service=service, options=options)
browser.get(START_URL)

time.sleep(5)

data = []
# BeautifulSoup Object
soup = BeautifulSoup(browser.page_source, "html.parser")

# Find <table>
bright_star_table = soup.find("table", attrs={"class", "wikitable"})

# Find <tbody>
table_body = bright_star_table.find("tbody")

# Find <tr>
table_rows = table_body.find_all("tr")


for tr in table_rows:
    temp_list = []
    for td in tr.find_all("td"):
        try:
            temp_list.append(str(td.contents[0].text).strip())

        except:
            temp_list.append("")

    data.append(temp_list)

print("data:", data)
headers = [
    "v mag",
    "name",
    "bayer designation",
    "distance",
    "spectral class",
    "mass",
    "raduis",
    "luminousity",
]
df = pd.DataFrame(data, columns=headers)
df.to_csv("wiki_data.csv", index=True, index_label="id")
