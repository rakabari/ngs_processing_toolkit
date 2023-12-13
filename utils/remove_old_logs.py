#!/home/sbsuser/venv/bin/python3.11
import os
from datetime import datetime


def remove_old_logs(dir_path=os.getcwd()):
    """
    Remove old script logs.

    Args:
        dir_path (str): The directory path to search for log files. Defaults to the current working directory.

    """
    logs_dir = os.path.join(dir_path, 'logs')

    for entry in os.scandir(logs_dir):
        if not entry.is_file() or not entry.name.endswith('.log'):
            continue  # skip directories and non-log files

        # Get last modified time of log file
        mtime = datetime.fromtimestamp(entry.stat().st_mtime)

        # Remove logs older than 1 hour and without errors in them
        with open(entry.path, 'r') as f:
            log_contents = f.read().lower()
        if (datetime.now() - mtime).total_seconds() / 3600 > 1 and 'error' not in log_contents:
            os.remove(entry.path)

        # Remove logs older than 15 days (360 hours) regardless of errors
        if (datetime.now() - mtime).total_seconds() / 3600 > 360:
            os.remove(entry.path)

    # Remove big (>2MB) program (e.g. RunUploader.jar) logs
    for entry in os.scandir(dir_path):
        if not entry.is_file() or not entry.name.endswith('.log'):
            continue  # skip directories and non-log files

        size_mb = entry.stat().st_size/(1024*1024)
        if size_mb > 2:
            os.remove(entry.path)
