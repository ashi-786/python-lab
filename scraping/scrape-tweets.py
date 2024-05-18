#importing required libraries(modules)
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec

chromeOptions = Options()
chromeOptions.add_argument("--start-maximized")

logs = open("C:/Users/ghani/Desktop/logs.txt", 'a')
driver = webdriver.Chrome(options=chromeOptions)

try:
    tweeter_url = "https://twitter.com/login"
    driver.get(tweeter_url)

    wait = WebDriverWait(driver, 5)
    username_input = wait.until(ec.visibility_of_element_located((By.NAME, "session[username_or_email]")))
    username_input.send_keys('@Grish29')
    password_input = wait.until(ec.visibility_of_element_located((By.NAME, "session[password]")))
    password_input.send_keys('babussb29492')
    login_button = wait.until(ec.visibility_of_element_located((By.XPATH, "//div[@data-testid='LoginForm_Login_Button']")))
    login_button.click()

    search_input = wait.until(ec.visibility_of_element_located((By.XPATH, "//div/input[@data-testid='SearchBox_Search_Input']")))
    search_input.clear()
    search_input.send_keys("olympics2020" + Keys.ENTER)
    tweet_divs = driver.find_elements_by_xpath("//div[@data-testid='tweet']")
    for div in tweet_divs:
        spans = div.find_elements_by_xpath(".//div/span")
        tweets = ''.join([span.text for span in spans])
        print(tweets)    

except Exception as e:
    logs.write(f"Error during login: {str(e)}\n")

# hyipexplorer using selenium
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# url = "https://www.hyipexplorer.com"
# data = []

# driver = webdriver.Chrome()
# try:
# WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/table[5]/tbody/tr[7]/td/table')))
# td1 = driver.find_elements(By.XPATH, '//*[@id="content"]/table[5]/tbody/tr[7]/td/table')
# print(td1)
# img1 = td1.find_element(By.TAG_NAME, "img")
# print(img1)
# except:
    # print("Page couldn't reload")