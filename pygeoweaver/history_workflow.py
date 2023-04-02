import json
import requests
import pandas as pd
from IPython.display import display
from ipywidgets import interact, Dropdown, Select, Button, HBox, Layout, Text, VBox, Output

geoweaver_url = 'http://localhost:8070/Geoweaver/web/'
workflow_selection = Select(description="Workflow")
process_selection = Select(description="Process")
_workflow = dict()
workflow_names = list()

output = Output()
workflow_history_df = pd.DataFrame()

_process = dict()
process_names = list()

def _update_options():
    workflow_lst = requests.post(geoweaver_url + "list", data={'type': 'workflow'}).json()
    for w in workflow_lst:
        _workflow[w['name']] = w['id']
        workflow_names.append(w['name'])
    workflow_selection.options = workflow_names
    update_process_options()


def update_process_options():
    process_names.clear()
    id = _workflow[workflow_selection.value]
    req = requests.post(geoweaver_url + "detail", data={'type': 'workflow', 'id': id})
    req_json = json.loads(req.text)
    for k, v in req_json.items():
        if k == "edges":
            edges = json.loads(v)
            for e in edges:
                _process[e['source']['title']] = e['source']['id']
                process_names.append(e['source']['title'])
    process_selection.options = process_names


def get_workflow_history():
    workflow_id = _workflow[workflow_selection.value]
    payload = {'id': workflow_id, 'type': 'workflow'}
    req = requests.post(geoweaver_url + "logs", data=payload, params=payload)


def setup_dataframe(df):
    out = Output()
    with out:
        display(df)
    return out


_update_options()
get_workflow_history()


def history_workflow():
    VBox([workflow_selection, setup_dataframe(workflow_history_df)])