# import threading
# import queue
import requests

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
import concurrent.futures

with open("valid_proxies.txt", "r") as f:
    proxy = f.read().split("\n")
    proxies = [p for p in proxy]

def extract(proxy):
    try:
        print(f"Using {proxy}")
        r = requests.get("https://httpbin.org/ip", proxies={"http": proxy}, timeout=2)
        print(r.json(), "ok")
    except:
        pass
    return proxy

with concurrent.futures.ThreadPoolExecutor() as exectr:
    exectr.map(extract, proxies)
