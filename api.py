import requests
import pandas as pd
from urllib.parse import urljoin
from configparser import ConfigParser
import json

# Read config file
config_object = ConfigParser()
config_object.read('config.ini')
api = config_object["CHROMEDRIVER"]

# response = requests.get("http://api.open-notify.org/this-api-doesnt-exist")

class Petfinder:


    def __init__(self):
        r"""
        Initialization method of the :code:`Petfinder` class.
        Parameters
        ----------
        key : str
            API key given after `registering on the PetFinder site <https://www.petfinder.com/developers/api-key>`_
        secret : str
            Secret API key given in addition to general API key. The secret key is required as of V2 of
            the PetFinder API and is obtained from the Petfinder website at the same time as the access key.
        """
        self.key = 'cWpdAa8nF7FeLyizuljgnKrosH7HbEGXN4aqaVEZGRbPgVk3hf'
        self.secret = 'bzeNrwFOlOwCgcD7EhVgA4mOOHmBolMGTBiJDIq7'
        self._host = 'http://api.petfinder.com/v2/'
        self._auth = self._authenticate()


    def _authenticate(self):
        r"""
        Internal function for authenticating users to the Petfinder API.
        Raises
        ------
        Returns
        -------
        str
            Access token granted by the Petfinder API. The access token stays live for 3600 seconds, or one hour,
            at which point the user must reauthenticate.
        """
        endpoint = 'oauth2/token'

        self.url = urljoin(self._host, endpoint)

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.key,
            'client_secret': self.secret
        }
        r = requests.post(self.url, data=data)

        # if r.status_code == 401:
        #     raise PetfinderInvalidCredentials(message=r.reason, err='Invalid Credentials')

        return r.json()['access_token']

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


test = Petfinder()
new_animals = []
i = 1
while i <= 10:
    r = requests.get(test._host+'animals?page='+str(i), headers={'Authorization': 'Bearer ' + test._auth})
    i += 1
    # jprint(r.json())
    data = r.json()
    # data = json.load(r)
    # df = pd.DataFrame.from_dict(data, orient='index')
    # print(df)
    animals = data['animals']
    for animal in animals:
        gender = animal['gender']
        fixed = animal['attributes']['spayed_neutered']

        if fixed == 'False':
            fixed = 'Unknown'
        elif gender == 'Female' and fixed == 'True':
            fixed = 'Spayed'
        else:
            fixed = 'Neutered'

        new_animals.append({'Animal ID': animal['id'], 'Breed': animal['breeds']['primary'], 'Sex': gender,
                            'Age': animal['age'], 'Fixed': fixed, 'Intake Status': animal['status']})



df = pd.DataFrame(new_animals)
print(df)


