import requests
from constants import geoweaver_url
from IPython.display import display
import pandas as pd


def list_process():
    geoweaver_listing_url = geoweaver_url + "list"
    req = requests.post(geoweaver_listing_url, data={'type': 'process'}).json()
    pd_json = pd.DataFrame(req)
    return display(pd_json)



