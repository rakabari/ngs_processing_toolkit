#!/home/sbsuser/venv/bin/python3.11
# import pypaths
from utils.global_vars import LOGS
import os

# Quick and Dirty script to create crontab,
# Manually place the printed statements in crontab

home_rel = '~/scripts'
home_abs = '/home/sbsuser'
cronlogs_dir = f'{home_abs}/scripts/logs/cronlogs'
cronjobs_dir = f'{home_abs}/scripts/cronjobs'


os.makedirs(cronlogs_dir, exist_ok=True)

for file in os.listdir(cronjobs_dir):
    if 'run_' in file:
        cronlog_name = file.replace('run_', '').replace('.py', '.log')
        source = '. ~/.bashrc;'
        crontab = f'*/1 * * * * {source} {home_rel}/cronjobs/{file} &> {home_rel}/logs/cronlogs/{cronlog_name}'
        print(crontab)

'''


#NEW
*/12 1-23/2 * * * . ~/.bashrc; ~/scripts/cronjobs/run_bcl_conversion.py &> ~/scripts/logs/cronlogs/bcl_conversion.log
*/21 1-23/2 * * * . ~/.bashrc; ~/scripts/cronjobs/run_cgw_uploader.py &> ~/scripts/logs/cronlogs/cgw_uploader.log
*/5 0-22/2 * * * . ~/.bashrc; ~/scripts/cronjobs/run_pending_logs.py &> ~/scripts/logs/cronlogs/pending_logs.log
*/7 0-22/2 * * * . ~/.bashrc; ~/scripts/cronjobs/run_cgw_api.py &> ~/scripts/logs/cronlogs/cgw_api.log
*/12 0-22/2 * * * . ~/.bashrc; ~/scripts/cronjobs/run_cgw_checklist.py &> ~/scripts/logs/cronlogs/cgw_checklist.log
*/17 0-22/2 * * * . ~/.bashrc; ~/scripts/cronjobs/run_cgw_sql.py &> ~/scripts/logs/cronlogs/cgw_sql.log
*/22 0-22/2 * * * . ~/.bashrc; ~/scripts/cronjobs/run_foundation.py &> ~/scripts/logs/cronlogs/foundation.log
*/27 0-22/2 * * * . ~/.bashrc; ~/scripts/cronjobs/run_sav.py &> ~/scripts/logs/cronlogs/sav.log
*/32 0-22/2 * * * . ~/.bashrc; ~/scripts/cronjobs/run_manage_storage.py &> ~/scripts/logs/cronlogs/manage_storage.log


In these entries:
*/15 in the minute field means "every 15 minutes."
1-23/2 in the hour field for script2.py specifies that it will run at 1 AM, 3 AM, 5 AM, and so on, up to 11 PM (odd hours).
0-22/2 in the hour field for script6.py specifies that it will run at 12 AM, 2 AM, 4 AM, and so on, up to 10 PM (even hours).

'''
