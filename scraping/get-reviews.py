import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = "https://www.consumeraffairs.com/food/dominos.html"
all_pages_reviews = []

def scraper():
    driver = webdriver.Chrome()
    for i in range(1,3):
        pagewise_reviews = []
        url = f"{base_url}?page={str(i)}"
        driver.get(url)
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "rvw__top-text")))
        except:
            print(f"Reviews not found on page {i}")
            continue
        rev_divs = driver.find_elements(By.CLASS_NAME, "rvw__top-text")

        for review_div in rev_divs:
            review_text = review_div.find_element(By.TAG_NAME, "p").text
            pagewise_reviews.append(review_text)

        for j in range(len(pagewise_reviews)):
            all_pages_reviews.append(pagewise_reviews[j])
    # print(all_pages_reviews)
    driver.quit()
    return all_pages_reviews

# scraper()
reviews = scraper()
# print(reviews)
#storing to a pandas dataframe
i = range(1, len(reviews)+1)
reviews_df = pd.DataFrame({'review':reviews}, index=i)
print(reviews_df)

#Writing the content of the data frame to a text file
reviews_df.to_csv('reviews.csv', sep='t')