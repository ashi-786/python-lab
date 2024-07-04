# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
# from bs4 import BeautifulSoup

SCRAPEOPS_API_KEY = 'f1bd630d-7af0-4123-b4dd-6c8010bed171'
proxy_options = {
    'proxy': {
        'http': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'https': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'no_proxy': 'localhost:127.0.0.1'
    }
}
driver = webdriver.Chrome(seleniumwire_options=proxy_options)
base_url = "https://www.fotocasa.es"
links = []
# driver = webdriver.Chrome()

def scroll_and_wait(wait_time, scroll_step=500):
    scroll_start = 0
    while True:
        scroll_end = scroll_start + scroll_step
        driver.execute_script(f"window.scrollTo({scroll_start}, {scroll_end})")
        scroll_start = scroll_start + scroll_step
        time.sleep(wait_time)
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, "article")))
        article = len(driver.find_elements(By.TAG_NAME, "article"))
        if article == 30:
            break

# for i in range(1, 50):
url = f"https://www.fotocasa.es/es/comprar/viviendas/espana/todas-las-zonas/l/{1}"
try:
    driver.get(url)
    accept_cookies_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "didomi-notice-agree-button")))
    accept_cookies_button.click()
except: pass
driver.get(url)
scroll_and_wait(2)
articles = driver.find_elements(By.TAG_NAME, "article")
print(len(articles))
links.append([base_url+a.find_element(By.TAG_NAME, "a").get_attribute("href") for a in articles])
print(links)

driver.quit()