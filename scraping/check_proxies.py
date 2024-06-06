# import threading
# import queue
# import requests

# q = queue.Queue()
# valid = []

# with(open("proxy_list.txt", "r") as f):
#     proxies = f.read().split("\n")
#     for p in proxies:
#         q.put(p)

# def check():
#     global q
#     while not q.empty():
#         proxy = q.get()
#         try:
#             res = requests.get("http://ipinfo.io/json", proxies={"http": proxy, "https": proxy})
#         except:
#             continue
#         if res.status_code == 200:
#             print(proxy)

# for _ in range(10):
#     threading.Thread(target=check).start()

# Another Method
# import concurrent.futures

# with open("proxy_list.txt", "r") as f:
#     proxy = f.read().split("\n")
#     proxies = [p for p in proxy]

# def extract(proxy):
#     try:
#         print(f"Using {proxy}")
#         r = requests.get("https://httpbin.org/ip", proxies={"http": proxy}, timeout=2)
#         print(r.json(), "ok")
#     except:
#         pass
#     return proxy

# with concurrent.futures.ThreadPoolExecutor() as exectr:
#     exectr.map(extract, proxies)


import re

data = ['2 Beds', '2 Baths', '2,291.63 Sqft', '5.052 ac Lot Size']

# Define a function to extract digits with optional decimal (for lot size)
def extract_digits(text):
  """
  Extracts digits and optional decimal from a string, removing non-numeric characters.

  Args:
      text: The string to extract digits from.

  Returns:
      str: The extracted digits (including optional decimal), or an empty string if no match.
  """
  text = text.replace(",", "")
  match = re.search(r'\d+(?:\.\d+)?', text)  # Capture digits and optional decimal
  if match:
    return match.group()
  else:
    return ""  # Return empty string if no digits found

# Extract digits from each data point
for item in data:
    value = extract_digits(item)
    if "." in value:
        print(float(value))
    else:
       print(int(value))