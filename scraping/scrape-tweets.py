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

# table1 = soup.find_all("table", attrs={'class': 'hyip', 'cellspacing': '0', 'cellpadding': '0'})
# print(table1)
# req_data['stickyw.gif'] = url + table1[1].find("img", attrs={'alt': 'sticky'}).get('src')
# req_data['hyip-program'] = table1[1].find("a", class_=["hyip_program"]).text
# req_data['star-rating'] = url + table1[1].find("div", class_=["rating"]).img.get('src')
# req_data['reviews'] = table1[1].find("span", class_=["s9"]).text
# req_data['status'] = table1[1].find("div", class_=["status"]).text
# req_data['sslfree.gif'] = url + soup.find("img", attrs={'title': 'Free SSL valid: -212 days'}).get('src')

# stats = list(soup.find_all("table", attrs={'cellspacing': '2', 'cellpadding': '2'}))[1]
# req_data['stats'] = stats.text.strip()

# desc = list(soup.find_all("div", class_=["even"]))[1]
# req_data['shots'] = url + desc.img.get('src')
# req_data['description'] = desc.text.strip()

# link = list(soup.find_all("a", class_=["details"]))[1].get('href')
# req_data['program details'] = url+link

# monitored = list(soup.find_all("span", attrs={'class': 's9 gray'}))[1]
# req_data['monitored'] = monitored.text.strip()

# hbstatus = list(soup.find_all("div", class_=["a_"]))[1]
# req_data['hbstatus'] = hbstatus.text.strip()

# table = soup.find("div", id="content").find_all("table")[9]
# values.append(table.find_all("td", attrs={'valign': 'middle'})[1].find_all("div")[0].text.strip())
# values.append(table.find_all("td", attrs={'valign': 'middle'})[1].find_all("div")[1].text.strip())
# values.append(table.find_all("td", attrs={'valign': 'middle'})[1].find_all("div")[2].text.strip())
# values.append(table.find_all("div", class_=["a_jr"])[1].text.strip())
# values.append(table.find_all("td", attrs={'align': 'left'}))