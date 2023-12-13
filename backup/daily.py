#!/home/sbsuser/venv/bin/python3.11
import os
from utils.rsync_wrapper import backup
from utils.global_vars import HOME, BACKUP_DIR, DAILY_BACKUP_DIR

exclude_list = os.path.join(BACKUP_DIR, 'scheduled_exclude.txt')

backup(HOME, DAILY_BACKUP_DIR, exclude_list)
