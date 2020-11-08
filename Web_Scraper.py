
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
URL_DETAILS = "https://animalcare.lacounty.gov/view-our-animals/?animalCareCenter=ALL&animalType=ALL&sex=ALL&breed=ALL&animalAge=ALL&animalSize=ALL&animalID=&animalDetail="
CHROME_DRIVER = "C:\web-drivers\chromedriver.exe"


def get_animal_details(driver, ID_list):
    """
    get animal details from page by animal ID
    """
    # Initializing dictionary to store animal details
    animal_dict = {}

    # iterate over animal IDs and gather animal details
    for ID in ID_list:
        driver.get(URL_DETAILS+ID)
        time.sleep(1)
        elements = driver.find_elements_by_class_name('col-sm-12')
        time.sleep(1)
        details_list = []
        for i in elements:
            element_text = i.text
            if element_text != '':
                temp_list = element_text.split('\n')
                if len(temp_list) < 3:
                    details_list.append(temp_list)

        # puts animal details into user-friendly readable format
        clean_list = clean_animal_list(details_list)
        print(clean_list)
        animal_dict[ID] = clean_list

    # print full dictionary with animal IDs as keys and details as values
    print(animal_dict)


def clean_animal_list(details_list):
    """
    scrap animal detail list and store: breed, sex, age, fixed, location, intake date and availability date in new list
    """
    try:
        breed = details_list[1]
        sex = details_list[2]
        age = details_list[3]
        fixed = details_list[4]
        location = details_list[7]
        intake_date = details_list[9]
        available_date = details_list[10]
        return [breed[1], sex[1], age[1], fixed[1], location[1], intake_date[1], available_date[1]]
    except IndexError:
        return ['no result']


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
    except (TimeoutException, WebDriverException):
        print("Last page reached")
        return False


def main():

    # Initiates the connection to the host URL
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER)
    driver.get(URL)

    # view options for next page
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    # Initializing parameters for gathering animal IDs
    ID_list = []
    has_next_page = True

    # Gather animal IDs from every webpage
    while has_next_page:
        ID_list = get_animal_id(driver, ID_list)
        has_next_page = move_to_next_page(driver)

    # Gather animal details from individual animal pages
    get_animal_details(driver, ID_list)

    driver.quit()


if __name__ == '__main__':
    main()