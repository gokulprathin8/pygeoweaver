from geoweaver import execute_cli_command


def list_host():
    command_out, _ = execute_cli_command("list host")
    return command_out



