"""
Detail subcommand
"""
import json
import subprocess

import pandas as pd
import requests
from pygeoweaver.constants import *

from pygeoweaver.utils import (
    download_geoweaver_jar,
    get_geoweaver_jar_path,
    get_java_bin_path,
    get_root_dir, create_table,
)
import ipywidgets as widgets
from IPython.display import display, HTML


def detail_workflow(workflow_id):
    if not workflow_id:
        raise RuntimeError("Workflow id is missing")
    download_geoweaver_jar()
    url = f"{GEOWEAVER_DEFAULT_ENDPOINT_URL}/web/detail"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    workflow_id = "grlgu9mkbry3qe8qxdg1"
    type = "workflow"

    form_data = {'type': type, 'id': workflow_id}

    d = requests.post(url=url, data=form_data, headers=headers)
    d = d.json()
    d['nodes'] = json.loads(d['nodes'])
    try:
        from IPython import get_ipython
        if 'IPKernelApp' in get_ipython().config:
            table_html = create_table([d])
            table_output = widgets.Output()
            with table_output:
                display(HTML(table_html))
            display(table_output)
    except:
        df = pd.DataFrame([d])
        display(df)


def detail_process(process_id):
    if not process_id:
        raise RuntimeError("Process id is missing")
    download_geoweaver_jar()
    subprocess.run(
        [
            get_java_bin_path(),
            "-jar",
            get_geoweaver_jar_path(),
            "detail",
            f"--process-id={process_id}",
        ],
        cwd=f"{get_root_dir()}/",
    )


def detail_host(host_id):
    if not host_id:
        raise RuntimeError("Host id is missing")
    download_geoweaver_jar()
    subprocess.run(
        [
            get_java_bin_path(),
            "-jar",
            get_geoweaver_jar_path(),
            "detail",
            f"--host-id={host_id}",
        ],
        cwd=f"{get_root_dir()}/",
    )


def get_process_code(process_id):
    r = requests.post(
        f"{GEOWEAVER_DEFAULT_ENDPOINT_URL}/web/detail",
        data={"type": "process", "id": process_id},
    ).json()
    return r["code"]
