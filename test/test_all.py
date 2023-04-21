import uuid
import pytest
import subprocess
from pathlib import Path
from unittest.mock import Mock

from pygeoweaver.utils import download_geoweaver_jar, get_geoweaver_jar_path, get_home_dir, check_os, get_root_dir
from pygeoweaver.sc_detail import detail_host, detail_process, detail_workflow


#######################  utils  #######################
def parse_ascii_table(table_content):
    builder: list = list()
    keys: list = list()

    for idx, line in enumerate(table_content.splitlines()):
        if line in [str(), line.startswith('+')]:
            continue

        if line.startswith('|'):
            current_line = line.split('|')
            current_line = [c.strip() for c in current_line]
            current_line = [c for c in current_line if c]

            if idx == 2:
                keys = current_line
                continue
            for index, value in enumerate(keys):
                builder.append({
                    keys[index]: current_line[index]
                })
    return builder


#######################  fixtures  #######################
@pytest.fixture
def mocker():
    return Mock()


#######################  utils.py  #######################
def test_can_download_geoweaver():
    """
        Check if geoweaver can be downloaded from the hardcoded url from github
    :return: None    :rtype: None
    """
    download_geoweaver_jar()
    if not Path(get_geoweaver_jar_path()).is_file():
        raise FileNotFoundError("Geoweaver jar file failed to download")


def test_get_home_dir():
    """
        Should always return a STRING POSIX Path to home directory
    :return: None   :rtype: None
    """
    # return home POSIX path of OS
    assert Path.home() == Path(get_home_dir())


def test_check_os():
    # should always return an int
    assert type(check_os()) == int


#######################  sc_detail.py  #######################
def test_detail_workflow_with_valid_workflow(mocker):
    subprocess_mock = mocker.patch.object(subprocess, 'run')
    workflow_id = 'gr3ykr8dynu12vrwq11oy'  # id for snowcast
    detail_workflow(workflow_id=workflow_id)
    out, err = subprocess_mock.assert_called_once_with(
        ["java", "-jar", get_geoweaver_jar_path(), "detail", f"--workflow-id={workflow_id}"],
        cwd=f"{get_root_dir()}/"
    )


def test_detail_workflow_with_invalid_workflow(mocker):
    subprocess_mock = mocker.patch.object(subprocess, 'run')
    workflow_id = str(uuid.uuid4().hex)  # some random id
    detail_workflow(workflow_id=workflow_id)
    out, err = subprocess_mock.assert_called_once_with(
        ["java", "-jar", get_geoweaver_jar_path(), "detail", f"--workflow-id={workflow_id}"],
        cwd=f"{get_root_dir()}/"
    )
