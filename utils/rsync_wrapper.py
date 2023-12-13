#!/home/sbsuser/venv/bin/python3.11
import os
import subprocess
from utils.global_vars import S_DRIVE
from utils.mnt_win import mount_drive
from datetime import datetime


def backup(src, dst, excudefile):
    mount_drive(S_DRIVE)
    date_time = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    cmd = f'rsync -av --exclude-from={excudefile} {src} {dst}'
    subprocess.run(cmd, shell=True, check=True)
