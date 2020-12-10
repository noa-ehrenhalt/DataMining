# DataMining

DataMining is a Python project that scrapes the [LA county animal control website](https://animalcare.lacounty.gov/) and
 gathers details about available animals in Los Angeles County, California US.  It also utilizes the Petfinder API to 
 gather details about animals in shelters and rescue organizations partnered with Petfinder.

## Installation

Please download the [Chrome Driver](https://chromedriver.chromium.org/) for your machine and update the CHROME_DRIVER variable in the config.py file to reflect its path.

Update host, username, and password in config.py file.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

This project requires the use of a MySQL database.

## Usage

Run project's main.py file using python via the command line. 

Command line search filters available:

  -a : Animal ID as listed on the LA County Animal Control or Petfinder website. Retrieves only that particular animal and may not be used in conjunction with other search options.
  
  -b : Breed represented by the breed name in all capital letters.  See help for available breed names.
  
  -l : Location represented by the location name.  See help for available location names.
  
  -d : Retrieves data for animals with available dates in the recent number of days specified.  Parameter input must be an integer.

## About the project

The website used contains javascript, therefore BeautifulSoup (a popular python scraping package) was not suitable for this project. As a result, selenium was used to access the 
data for further usage. Data scraped from the LA County Animal Control file is saved to a .csv file and imported into a database.  In the Web_Scraper.py file there are wait and\or sleep statements in order to accommodate the page loading time.
  The project also uses the Petfinder API to gather information about animals listed on the Petfinder website.  An API key and secret code have been obtained 
  and included in the config file for this purpose.

