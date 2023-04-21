"""
The main function of pygeoweaver
To run in CLI mode. 
"""
import subprocess
from unittest.mock import patch

from pygeoweaver import detail_host, detail_process, detail_workflow
from pygeoweaver import export_workflow
from pygeoweaver import show_history
from pygeoweaver import import_workflow
from pygeoweaver import list_hosts, list_processes, list_workflows
from pygeoweaver import start, stop

import unittest


class TestPyGeoweaver(unittest.TestCase):

    @patch('pygeoweaver.utils.download_geoweaver_jar')
    @patch.object(subprocess, 'run')
    @patch('pygeoweaver.utils.get_geoweaver_jar_path')
    @patch('pygeoweaver.utils.get_root_dir')
    def test_detail_workflow(self, mock_get_root_dir, mock_get_geoweaver_jar_path, mock_subprocess_run,
                             mock_download_geoweaver_jar):
        workflow_id = 'workflow_id'
        mock_get_root_dir.return_value = '/root/dir'
        mock_get_geoweaver_jar_path.return_value = '/geoweaver/jar'
        detail_workflow(workflow_id)
        mock_download_geoweaver_jar.assert_called_once()
        mock_subprocess_run.assert_called_once_with(
            ["java", "-jar", "/geoweaver/jar", "detail", f"--workflow-id={workflow_id}"],
            cwd='/root/dir/')


if __name__ == "__main__":
    unittest.main()
