import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

url="https://finance.yahoo.com/sectors/technology/"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
section1 = soup.find("section", class_=["svelte-ekgvwx"])
section2 = soup.find("section", attrs={'data-testid' : 'investing-in'})
main_list = []

def subdata(tr):
    sub_list = []
    for td in tr:
        sub_list.append(td.text.strip())
    return sub_list

main_list.append(section1.h2.text.strip())
main_list.append(subdata(section1.find_all("th")))
trs = section1.tbody.find_all("tr")
for tr in trs:
    main_list.append(subdata(tr.find_all("td")))


main_list.append(section2.h2.text.strip())
main_list.append(section2.p.text.strip())
tables = section2.find_all("div", class_=["table-section-container"])
for table in tables:
    main_list.append(table.h3.text.strip())
    main_list.append(subdata(table.find_all("th")))
    trs = table.tbody.find_all("tr")
    for tr in trs:
        main_list.append(subdata(tr.find_all("td")))

# with open('yahoo-finance.json', 'w') as f:     
#     json.dump(main_list, f, indent=4)

main_list_df = pd.DataFrame(main_list)
print(main_list_df)
main_list_df.to_csv('yahoo-finance.csv', quoting=1, index=False)