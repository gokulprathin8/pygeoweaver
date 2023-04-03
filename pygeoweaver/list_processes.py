from geoweaver import execute_cli_command


def list_process():
    command_out, _ = execute_cli_command("list process")
    return command_out



