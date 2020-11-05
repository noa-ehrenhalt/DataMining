import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

URL = "https://animalcare.lacounty.gov/view-our-animals/?animalCareCenter=ALL&animalType=ALL&sex=ALL&breed=ALL&animalAge=ALL&animalSize=ALL&animalID=&pageNumber=1&animalDetail="
XPATH = "//html/body/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/div[3]/div/div[3]/div"
ANIMAL_DETAIL_CLASS = "animalDetailItem"
# SELECTOR = "#page-24749 > div.grve-section.grve-fullwidth-background.grve-bg-none > div > div > div > div > div > div.row-fluid > div > div > div > div > div:nth-child(14) > div > div.animalDetails.animalSearchDetail > div:nth-child(1)"
ID_list = []

# Initiates the connection to the host URL
driver = webdriver.Chrome(executable_path='C:\web-drivers\chromedriver.exe')
driver.get(URL)









options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

page_num = 1
while True:


    wait = WebDriverWait(driver, 10)
    elem = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH)))

    elements = driver.find_elements_by_class_name(ANIMAL_DETAIL_CLASS)
    for item in elements:
        element_text = item.text
        if 'ID' in element_text:
            ID_num = element_text.split(' ')
            ID_list.append(ID_num[-1])
            print(ID_num[-1])
    try:
        driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/div[2]/ul/li[12]/span"))))
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/div[2]/ul/li[12]/span").click()
        time.sleep(1)
        print(page_num)
        page_num += 1
        print("Navigating to Next Page")
    except (TimeoutException, WebDriverException) as e:
        print(page_num)
        print("Last page reached")
        break

print(ID_list)
driver.quit()





driver.quit()