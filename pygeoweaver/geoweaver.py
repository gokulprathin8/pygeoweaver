import os
import subprocess


def execute_cli_command(command):
    homedir = os.path.expanduser('~')
    jar_path = os.path.join(homedir, 'geoweaver.jar')
    # join command
    process = subprocess.Popen(
        jar_path.split() + command.split(), stdout=subprocess.PIPE
    )
    out, err = process.communicate()
    return out, err
