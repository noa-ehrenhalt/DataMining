# DataMining

DataMining is a Python project that scrapes [LA county animal control](https://animalcare.lacounty.gov/) and gathers details about all available animals.

## Installation

Please download the [Chrome Driver](https://chromedriver.chromium.org/) for your machine and update the CHROME_DRIVER variable in the Web_Scraper.py file to reflect its path.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

## Usage

Run project using python. 

Print statements have been incorporated into the code to show the progress of the program implementation. 

## About the project

The website used contains javascript, therefore BeautifulSoup (a popular python sraping package) was not suitable for this project. As a result, selenium was used to access the 
data for further usage. In the Web_Scraper.py file there are wait and\or sleep statements in order to accommodate the page loading time.

