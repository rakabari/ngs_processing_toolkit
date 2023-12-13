#!/home/sbsuser/venv/bin/python3.11
import os
from pathlib import Path
from global_vars import LOGS


def create_log_directory(file_path):
    """
    Checks if a log directory exists for a script.
    If not, creates a log directory under the 'LOGS' directory.
    """

    # Obtain the script directory name from the script path
    dir_name = Path(os.path.dirname(file_path)).resolve().stem

    # Define the log directory path
    log_dir_path = os.path.join(LOGS, dir_name)

    # Create the log directory if it doesn't already exist
    Path(log_dir_path).mkdir(parents=True, exist_ok=True)
