def execute_command_and_capture(command: str) -> str:
    """Execute a command and capture the output.

    Args:
        command (str): The command to execute.

    Returns:
        str: The output of the command.
    """
    import subprocess

    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True,
    )

    return result.stdout


def format_memory(memory: int) -> str:
    """Memory is already bassed in as MB"""
    if memory > 1024:
        return f'{memory // 1024}GB'
    return f'{memory}MB'
