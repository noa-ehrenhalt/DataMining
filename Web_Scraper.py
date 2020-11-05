
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

URL = "https://animalcare.lacounty.gov/view-our-animals/?animalCareCenter=ALL&animalType=ALL&sex=ALL&breed=ALL&animalAge=ALL&animalSize=ALL&animalID=&pageNumber=1&animalDetail="
XPATH_ANIMAL_ID = "//html/body/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/div[3]/div/div[3]/div"
ANIMAL_DETAIL_CLASS = "animalDetailItem"
XPATH_NEXT_PAGE = "/html/body/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/div[2]/ul/li[12]/span"


def get_animal_id(driver, ID_list):
    """stores animal IDs from webpage into list
    """
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_ANIMAL_ID)))

    elements = driver.find_elements_by_class_name(ANIMAL_DETAIL_CLASS)
    for item in elements:
        element_text = item.text
        if 'ID' in element_text:
            ID_num = element_text.split(' ')
            ID_list.append(ID_num[-1])
            print(ID_num[-1])
    return ID_list


def move_to_next_page(driver):
    """move to next page, returns true if has next page and false when reached last page
    """
    try:
        driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, XPATH_NEXT_PAGE))))
        driver.find_element_by_xpath(XPATH_NEXT_PAGE).click()
        time.sleep(1)
        print("Navigating to Next Page")
        return True
    except (TimeoutException, WebDriverException) as e:
        print("Last page reached")
        return False


def main():

    # Initiates the connection to the host URL
    driver = webdriver.Chrome(executable_path='C:\web-drivers\chromedriver.exe')
    driver.get(URL)

    # view options for next page
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    # Initializing parameters for gathering animal IDs
    ID_list = []
    has_next_page = True

    while has_next_page:
        ID_list = get_animal_id(driver, ID_list)
        has_next_page = move_to_next_page(driver)

    driver.quit()

if __name__ == '__main__':
    main()