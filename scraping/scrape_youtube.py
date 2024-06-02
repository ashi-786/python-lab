# import requests
# from bs4 import BeautifulSoup as bs
# base_url = "https://www.youtube.com/watch?v="
# r = requests.get(base_url+video_id)
# # print(r.status_code)
# soup = bs(r.content, "lxml")
# watch_metadata = soup.find("ytd-watch-metadata")
# print(watch_metadata)

import googleapiclient.discovery
import googleapiclient.errors
import json

# Free YouTube Data API having limited Quota, can be created using Google Developer Console
Api = "YOUR-API-KEY"
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=Api)
video_id = "FbtCl9jJyyc"
# Video stats
# YouTube has made the decision to hide public dislike counts to avoid "dislike attacks" targeting creators.
request = youtube.videos().list(
    part="snippet,statistics",
    id=video_id
)
res = request.execute()
keys = ["title", "description", "publishedAt", "viewCount", "likeCount", "commentCount", "comments"]
vals = []
vals.append(res['items'][0]['snippet']['title'])
vals.append(res['items'][0]['snippet']['description'])
vals.append(res['items'][0]['snippet']['publishedAt'])
vals.append(res['items'][0]['statistics']['viewCount'])
vals.append(res['items'][0]['statistics']['likeCount'])
vals.append(res['items'][0]['statistics']['commentCount'])

# Video comments
req2 = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id
)
res2 = req2.execute()
print(res2)
comments = []

for item in res2['items']:
    comments.append({
        "text": item['snippet']['topLevelComment']['snippet']['textDisplay'],
        "likeCount": item['snippet']['topLevelComment']['snippet']['likeCount']
    })
vals.append(comments)
data = {keys[i]:vals[i] for i in range(len(keys))}

with open("yt_video_details.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)