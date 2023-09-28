from subprocess import run, PIPE


def execute_bash(command: str):
    """Execute the command (a string) in a bash subshell"""
    p = run(command, stdout=PIPE, stderr=PIPE, timeout=60, shell=True)
    return (p.stderr + p.stdout).decode()


def finish(result: str):
    """Finish execution and return the result"""
    return result
