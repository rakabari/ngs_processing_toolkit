#!/home/sbsuser/venv/bin/python3.11
import os
import subprocess

dirs = ['boot', 'etc',  'lib', 'opt',
        'sbin', 'srv', 'var', 'bin',
        'lib64', 'usr', 'home']

'''
/media, /mnt, /run, /snap, /sys, /proc, /dev, /afs: 
These directories are typically system-specific and may not contain user data or configuration that needs to be backed up. 
You can often exclude them from your backup.
'''

for d in dirs:
    cmd = f'sudo find /{d} -type d -exec du -sh' + \
        " {} " + f'\; > {d}.txt'
    print(cmd)
    # subprocess.run(cmd, shell=True, check=True)
