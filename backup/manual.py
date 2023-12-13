#!/home/sbsuser/venv/bin/python3.11
import os
from utils.rsync_wrapper import backup
from utils.global_vars import BACKUP_DIR, MANUAL_BACKUP_DIR

exclude_list = os.path.join(BACKUP_DIR, 'manual_exclude.txt')

backup('/', MANUAL_BACKUP_DIR, exclude_list)
