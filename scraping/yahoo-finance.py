import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

url="https://finance.yahoo.com/sectors/technology/"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
main_list = []

def extract(element):
    keys  = [th.text.strip() for th in element.find_all("th")]
    values = [[td.text.strip() for td in tr.find_all("td")] for tr in element.tbody.find_all("tr")]
    for value in values:
        data = {keys[i]: value[i] for i in range(len(keys))}
        main_list.append(data)

# data.append(section1.h2.text.strip())
extract(soup.find("section", class_=["svelte-ekgvwx"]))
tables = soup.find_all("div", class_=["table-section-container"])
# data.append(table.h3.text.strip())
for table in tables:
    extract(table)

# print(main_list)

with open('./media/yahoo-finance.json', 'w') as f:     
    json.dump(main_list, f, indent=4)

data_df = pd.DataFrame(main_list)
data_df.to_csv('./media/yahoo-finance.csv', index=False)