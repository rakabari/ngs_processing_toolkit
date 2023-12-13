#!/home/sbsuser/venv/bin/python3.11
import os
import subprocess

from utils.global_vars import S_DRIVE
from utils.mnt_win import mount_drive


mount_drive(S_DRIVE)

# exclude_list = '/home/sbsuser/scripts/backup/exclude.txt'
# src = '/home/sbsuser'
# dst = '/mnt/isiloncwb01_NGSData/ra2/backups/rhel'

# daily = os.path.join(dst, 'daily')
# weekly = os.path.join(dst, 'weekly')
# monthly = os.path.join(dst, 'monthly')
# quarterly = os.path.join(dst, 'quarterly')
# yearly = os.path.join(dst, 'yearly')

# cmd = f'rsync -av --exclude-from={exclude_list} {src} {daily}'
# print(cmd)


exclude_list = '/home/sbsuser/scripts/backup/exclude2.txt'
src = '/'
dst = '/mnt/isiloncwb01_NGSData/ra2/backups/rhel'

daily = os.path.join(dst, 'daily')
weekly = os.path.join(dst, 'weekly')
monthly = os.path.join(dst, 'monthly')
quarterly = os.path.join(dst, 'quarterly')
yearly = os.path.join(dst, 'yearly')

cmd = f'sudo rsync -avq --delete --exclude-from={exclude_list} {src} {daily} > cron.log'
subprocess.run(cmd, shell=True, check=True)
