import os
import requests
import webbrowser
from constants import geoweaver_url
from IPython.display import display, FileLink
from ipywidgets import interact, Dropdown, Select, Button, HBox, Layout

workflow_selection = Select()
_workflow = dict()
workflow_names = list()


def _update_options():
    workflow_lst = requests.post(geoweaver_url + "list", data={'type': 'workflow'}).json()
    for w in workflow_lst:
        _workflow[w['name']] = w['id']
        workflow_names.append(w['name'])
    workflow_selection.options = workflow_names


_update_options()


def on_button_click(_):
    home_directory = os.path.expanduser('~')
    workflow_id = _workflow[workflow_selection.value]
    req = requests.post(geoweaver_url + "downloadworkflow",
                        data={'id': workflow_id, 'option': 'workflowwithprocesscodeallhistory'}, stream=True)
    file_path = req.text.split('download/')[1]
    sys_path = os.path.join(home_directory, 'gw-workspace', file_path)
    display(FileLink(sys_path))
    webbrowser.open('file://' + sys_path)


layout = Layout(width='auto', height='40px')  # set width and height
download_button = Button(description=f"Download workflow", layout=layout, icon='download')
download_button.on_click(on_button_click)


def export_workflow():
    HBox([workflow_selection, download_button])
