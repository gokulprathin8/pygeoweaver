import requests
from IPython.display import display
import pandas as pd

from pygeoweaver.constants import geoweaver_url


def list_workflow():
    geoweaver_listing_url = geoweaver_url + "list"
    req = requests.post(geoweaver_listing_url, data={'type': 'workflow'}).json()
    pd_json = pd.DataFrame(req)
    return display(pd_json)



