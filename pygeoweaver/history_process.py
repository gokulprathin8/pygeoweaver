import os
import json
import requests
import webbrowser
from IPython.display import display
from ipywidgets import interact, Dropdown, Select, Button, HBox, Layout, Text, VBox, Output

geoweaver_url = 'http://localhost:8070/Geoweaver/web/'
workflow_selection = Select(description="Workflow")
process_selection = Select(description="Process")
_workflow = dict()
workflow_names = list()

_process = dict()
process_names = list()

output = Output()


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


def on_process_change(change):
    if change['type'] == 'change' and change['name'] == 'value':
        with output:
            output.clear_output()
            get_history()


process_selection.observe(on_process_change)


def get_history():
    id = _process[process_selection.value]
    params = {'type': 'process', 'id': id}
    req = requests.post(geoweaver_url + "logs", data=params, params=params)
    df = pd.DataFrame(req.json())
    with output:
        output.clear_output()
        if not df.empty:
            display(df)
        else:
            print("No history data found.")


def on_workflow_change(change):
    if change['type'] == 'change' and change['name'] == 'value':
        update_process_options()


workflow_selection.observe(on_workflow_change, names='value')

_update_options()

VBox([workflow_selection, process_selection, output])
