import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

URL = "https://animalcare.lacounty.gov/view-our-animals/"
XPATH = "//html/body/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/div[3]/div/div[3]/div"
ANIMAL_DETAIL_CLASS = "animalDetailItem"

# Initiates the connection to the host URL
driver = webdriver.Chrome(executable_path='C:/Users/arian/Downloads/chromedriver1/chromedriver.exe')
driver.get(URL)
wait = WebDriverWait(driver, 10)
elem = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH)))

elements = driver.find_elements_by_class_name(ANIMAL_DETAIL_CLASS)

ID_list = []
for item in elements:
    element_text = item.text
    if 'ID' in element_text:
        ID_num = element_text.split(' ')
        ID_list.append(ID_num[-1])
        print(ID_num[-1])



