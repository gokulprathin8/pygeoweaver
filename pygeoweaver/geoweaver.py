import os
import subprocess


def execute_cli_command(command):
    homedir = os.path.expanduser('~')
    jar_path = os.path.join(homedir, 'geoweaver.jar')
    command_builder = jar_path.split() + command.split()
    print(f"Executing CLI command {command_builder}")
    # join command
    process = subprocess.Popen(
        command_builder, stdout=subprocess.PIPE
    )
    out, err = process.communicate()
    return out, err
