"""
Scrapes animal data from LA County Animal Control website
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException, NoAlertPresentException, \
    StaleElementReferenceException
import sys
import csv
import animal_db
import os
from configparser import ConfigParser
import logging

logger = logging.getLogger(__name__)

# Read config file
config_object = ConfigParser()
config_object.read('config.ini')
cdrvr = config_object["CHROMEDRIVER"]

CDIR = os.getcwd()
URL = "https://animalcare.lacounty.gov/view-our-animals/?animalCareCenter=ALL&animalType=ALL&sex=ALL&breed=ALL" \
      "&animalAge=ALL&animalSize=ALL&animalID=&pageNumber=1&animalDetail="
XPATH_ANIMAL_ID = "//html/body/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/" \
                  "div[3]/div/div[3]/div"
ANIMAL_DETAIL_CLASS = "animalDetailItem"
XPATH_NEXT_PAGE = "/html/body/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/" \
                  "div[2]/ul/li[12]/span"
URL_DETAILS = "https://animalcare.lacounty.gov/view-our-animals/?animalCareCenter=ALL&animalType=ALL&sex=ALL" \
              "&breed=ALL&animalAge=ALL&animalSize=ALL&animalID=&animalDetail="
CHROME_DRIVER = "{}".format(cdrvr['url'])
CSV_COLUMNS = ['Animal ID', 'Breed', 'Sex', 'Age', 'Fixed', 'Intake Status', 'Location', 'Intake Date', 'Available Date']


def get_animal_details(driver, id_list):
    """
    get animal details from page by animal ID
    """
    # Initializing dictionary to store animal details
    animal_list = []

    # iterate over animal IDs and gather animal details
    for aid in id_list:
        driver.get(URL_DETAILS+aid)
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
        clean_list = clean_animal_list(aid, details_list)
        logger.info(clean_list)
        animal_list.append(clean_list)

    # print full dictionary with animal IDs as keys and details as values
    return animal_list


def clean_animal_list(aid, details_list):
    """
    scrape animal detail list and store: breed, sex, age, fixed, intake status, location, intake date and availability date and store
    in a dictionary
    """
    try:
        return {'Animal ID': aid, 'Breed': details_list[1][1], 'Sex': details_list[2][1], 'Age': details_list[3][1],
                'Fixed': details_list[4][1], 'Intake Status': details_list[5][1], 'Location': details_list[7][1], 'Intake Date': details_list[9][1],
                'Available Date': details_list[10][1]}
    except IndexError:
        return {}


def get_animal_id_list(driver, id_list, database_ids):
    """stores animal IDs from webpage into list
    """
    wait = WebDriverWait(driver, 10)
    wait.until(ec.element_to_be_clickable((By.XPATH, XPATH_ANIMAL_ID)))

    elements = driver.find_elements_by_class_name(ANIMAL_DETAIL_CLASS)
    for item in elements:
        element_text = item.text
        if 'ID' in element_text:
            id_num = element_text.split(' ')
            if id_num[-1] not in database_ids:
                id_list.append(id_num[-1])
                logger.info(id_num[-1])
    return id_list


def move_to_next_page(driver):
    """move to next page, returns true if has next page and false when reached last page
    """
    try:
        driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).
                              until(ec.element_to_be_clickable((By.XPATH, XPATH_NEXT_PAGE))))
        driver.find_element_by_xpath(XPATH_NEXT_PAGE).click()
        time.sleep(1)

        # Check for last page alert pop-up
        try:
            driver.switch_to.alert.accept()
            time.sleep(0.5)
            logger.info('Last page')
            return False
        except NoAlertPresentException:
            return True

    except StaleElementReferenceException:
        return True
    except (TimeoutException, WebDriverException):
        logger.info('Last page')
        return False


def main():
    try:
        # Initiates the connection to the host URL
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER)
        driver.get(URL)
    except WebDriverException:
        print('Cannot reach URL: {}'.format(URL))
        print('See README, requires chrome driver installation')
        sys.exit(1)

    # view options for next page
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    # Get existing animals from database
    database_ids = animal_db.get_aids()

    # Initializing parameters for gathering animal IDs
    id_list = []
    has_next_page = True

    # Gather animal IDs from every webpage
    while has_next_page:
        id_list = get_animal_id_list(driver, id_list, database_ids)
        has_next_page = move_to_next_page(driver)

    # Gather animal details from individual animal pages
    animal_dict = get_animal_details(driver, id_list)

    # Create CSV file to store data
    csv_file = '{}\\animal_data.csv'.format(CDIR)
    with open(csv_file, 'wt') as write:
        write_file = csv.DictWriter(write, fieldnames=CSV_COLUMNS)
        write_file.writeheader()

        # store animal data in CSV file
        for row in animal_dict:
            write_file.writerow(row)

    driver.quit()



