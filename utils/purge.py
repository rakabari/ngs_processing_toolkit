#!venv/bin/python3.10
import subprocess


cmd = 'sudo rm -rf /var/lib/mysql/binlog.*'
subprocess.run(cmd, shell=True, check=True)
