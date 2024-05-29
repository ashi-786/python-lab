import requests
import re
import json

url = "https://www.caballoria.com/_api/cloud-data/v2/items/query"
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
  'authorization': 'wixcode-pub.346b906df540d4fff69a62c7115b9b350ae0c735.eyJpbnN0YW5jZUlkIjoiNzc2YWQ0ODUtZWU5MC00MTBjLTgwMzAtZmZmYjNlYjE0N2VhIiwiaHRtbFNpdGVJZCI6IjkwN2FkZjk0LTZkNmEtNGE4YS04NGUwLWQ1Yzk2ZTk5ZmJhZiIsInVpZCI6bnVsbCwicGVybWlzc2lvbnMiOm51bGwsImlzVGVtcGxhdGUiOmZhbHNlLCJzaWduRGF0ZSI6MTcxNjg5NDYzNTgwMCwiYWlkIjoiNDI0OTAwYTktMjU4MS00ZWZiLTk5MmUtNmRlMzc0MzhlMTgxIiwiYXBwRGVmSWQiOiJDbG91ZFNpdGVFeHRlbnNpb24iLCJpc0FkbWluIjpmYWxzZSwibWV0YVNpdGVJZCI6ImZkZjA1NzU2LTE0NGItNDdiYi1hNTU1LTk1YWFiNjY0YzVmYyIsImNhY2hlIjpudWxsLCJleHBpcmF0aW9uRGF0ZSI6bnVsbCwicHJlbWl1bUFzc2V0cyI6IlNob3dXaXhXaGlsZUxvYWRpbmcsQWRzRnJlZSxIYXNEb21haW4iLCJ0ZW5hbnQiOm51bGwsInNpdGVPd25lcklkIjoiOTU5ZjU2NDktZWJmMy00OGVmLWIxOTctM2NlYWUwNGE3MTY3IiwiaW5zdGFuY2VUeXBlIjoicHViIiwic2l0ZU1lbWJlcklkIjpudWxsLCJwZXJtaXNzaW9uU2NvcGUiOm51bGwsImxvZ2luQWNjb3VudElkIjpudWxsLCJpc0xvZ2luQWNjb3VudE93bmVyIjpudWxsLCJib3VuZFNlc3Npb24iOm51bGwsInNlc3Npb25JZCI6bnVsbCwic2Vzc2lvbkNyZWF0aW9uVGltZSI6bnVsbH0=',
  'Content-Type': 'application/json',
  'Accept': 'application/json, text/plain, */*'
}

keys = ["title", "description", "horse_id", "image_link", "category", "color", "gender", "race", "height", "suitablity", "education", "price", "age", "location", "x_ray", "full_papers"]
main_list = []

for offset in range(0, 9*7, 9):
    payload = json.dumps({
    "dataCollectionId": "Verkaufspferde",
    "query": {
        "paging": {
        "offset": offset,
        "limit": 9
        }
    }
    })
    try:
        r = requests.request("POST", url, headers=headers, data=payload)
        print(r.status_code)
        r = r.json()
        print(len(r["dataItems"]))
        for i in range(len(r["dataItems"])):
            vals = []
            data = r["dataItems"][i]["data"]
            vals.append(data["title"]) #title
            vals.append(data["beschreibung"]) #description
            vals.append(data["id"]) #horse_id
            vals.append(data["bild"]) #img_link
            vals.append(data["status"]) #category
            vals.append(data["farbe"]) #color
            vals.append(data["geschlecht"]) #gender
            vals.append(data["rasse"]) #race
            vals.append(int(re.search(r"\d+", data["stockmass"]).group())) #height
            vals.append(data["eignung"]) #suitability
            vals.append(data["ausbildung"]) #education
            price = data["preis"].replace(".", "")
            vals.append(int(re.search(r"\d+", price).group())) #price
            vals.append(int(re.search(r"\d+", data["alter"]).group())) #age
            vals.append(data["standort"]) #location
            vals.append(data["Verkaufspferde"]) #x_ray
            vals.append(data["papers"]) #full_papers
            main_list.append({keys[i]:vals[i] for i in range(len(keys))})
    except:
        pass

with open("horse_details.json", "w") as f:
    json.dump({"horse": main_list}, f, indent=4)
