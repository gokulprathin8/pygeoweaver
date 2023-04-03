from geoweaver import execute_cli_command


def list_workflow():
    command_out, _ = execute_cli_command("list workflow")
    return command_out



