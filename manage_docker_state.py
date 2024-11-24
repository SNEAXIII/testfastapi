import sys
from re import search
from subprocess import run


STR_CMD = r"wsl --list --verbose"
DOCKER_REGEX = r'docker-desktop\s+Running'
START_DOCKER = r'"C:\Program Files\Docker\Docker\frontend\Docker Desktop.exe" & pause'
KILL_WSL = "wsl --shutdown"
NOTHING_TO_DO = "echo Nothing to do with Docker Desktop and WSL!"

number_of_args = len(sys.argv) - 1

if number_of_args != 1:
    raise IndexError(f'You have to pass one parameter, instead of {number_of_args}')

param = sys.argv[1]
if param not in ("start", "stop"):
    raise ValueError("You have to use either 'start' or 'stop' parameter")

cmd_result = run(STR_CMD, shell=True, capture_output=True, text=True).stdout.replace("\x00", "")
is_docker_running = search(DOCKER_REGEX, cmd_result)

return_value = None
if param == "start" and not is_docker_running:
    return_value = START_DOCKER
elif param == "stop" and is_docker_running:
    return_value = KILL_WSL
else:
    return_value = NOTHING_TO_DO
sys.stdout.write(return_value)
sys.stdout.flush()
sys.exit(0)
