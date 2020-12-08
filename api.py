import requests
import pandas as pd
from urllib.parse import urljoin
from configparser import ConfigParser
import animal_db
import logging

logger = logging.getLogger(__name__)

# Read config file
config_object = ConfigParser()
config_object.read('config.ini')
api = config_object["API"]


class PetFinder:

    def __init__(self):
        """Constructs the necessary attributes for the PetFinder object
        """
        self.key = api['key']
        self.secret = api['secret']
        self._host = api['host']
        self._auth = self._authenticate()


    def _authenticate(self):
        """Internal function for authenticating users to the PetFinder API, access token which stays live for 1 hour
        """
        endpoint = 'oauth2/token'
        self.url = urljoin(self._host, endpoint)
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.key,
            'client_secret': self.secret
        }
        req = requests.post(self.url, data=data)
        return req.json()['access_token']


def get_petfinder_animals():
    test = PetFinder()
    database_ids = animal_db.get_aids()
    new_animals = []
    i = 1
    while i <= 10:
        r = requests.get(test._host + 'animals?page=' + str(i), headers={'Authorization': 'Bearer ' + test._auth})
        i += 1

        # get data from request in json file format
        data = r.json()
        animals = data['animals']
        for animal in animals:
            # check if animal already exists in database
            if animal['id'] not in database_ids:
                # store fixed data in accordance to Animal Shelter DB format
                gender = animal['gender']
                fixed = animal['attributes']['spayed_neutered']
                if fixed == 'False':
                    fixed = 'Unknown'
                elif gender == 'Female' and fixed == 'True':
                    fixed = 'Spayed'
                else:
                    fixed = 'Neutered'
                logger.info({'Animal ID': animal['id'], 'Breed': animal['breeds']['primary'], 'Sex': gender,
                                    'Age': animal['age'], 'Fixed': fixed, 'Intake Status': animal['status']})
                new_animals.append({'Animal ID': animal['id'], 'Breed': animal['breeds']['primary'], 'Sex': gender,
                                    'Age': animal['age'], 'Fixed': fixed, 'Intake Status': animal['status']})

    df = pd.DataFrame(new_animals)
    animal_db.mycursor.close()
    animal_db.mydb.close()
    return df









