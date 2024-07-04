from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

base_url = "https://www.fotocasa.es"
driver = webdriver.Chrome()
links = []

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