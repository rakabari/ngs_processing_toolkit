#!/home/sbsuser/venv/bin/python3.11
# import pypaths
import os
from datetime import datetime
from utils.global_vars import LOGS


def execute_script(script_path):
    """Execute a Python script in a Bash shell, 
    capturing stderr and stdout to a log file with a timestamp."""

    # Extract script name and create log path
    script_dir = os.path.dirname(script_path)
    script_name = os.path.basename(script_path)
    log_dir_name = os.path.splitext(script_name)[0]

    log_dir_path = os.path.join(LOGS, log_dir_name)
    os.makedirs(log_dir_path, exist_ok=True)

    log_name = f'{datetime.now().strftime("%m%d%Y_%H%M%S")}_{log_dir_name}.log'
    log_path = os.path.join(log_dir_path, log_name)

    # Copy Pypaths to script directory because cron does not recognize the paths
    # os.system(f'cp {os.path.abspath(pypaths.__file__)} {script_dir}')

    # Execute the script in a Bash shell and capture both stdout and stderr
    os.system(f'{script_path} &> {log_path}')

    # Remove logs older than 60 minutes
    os.system(f"find {log_dir_path} -mmin +60 -delete")
