#!/home/sbsuser/venv/bin/python3.11
import os
import pandas as pd
from datetime import datetime, timedelta
from utils.mnt_win import mount_drive
from utils.global_vars import S_DRIVE, S_LOGS, NGS_MYE


COL_RENAME = {'mrn': 'MRN',
              'firstname': 'Patient First Name ',
              'lastname': 'Patient Last Name',
              'acc_num': 'Accession',
              'dob': 'Patient DOB',
              'disease': 'Disease',
              'spectype': 'Specimen Type',
              'ord_fname': 'Requesting Physicians First Name',
              'ord_lname': 'Requesting Physicians Last Name',
              'part_description': '',
              'accession_date': 'Accession Date',
              'coll_date': 'Collection Date',
              'rec_date': 'Received Date'}

COL_FILTER = ['MRN',
              'Accession',
              'Patient First Name ',
              'Patient Last Name',
              'Patient DOB',
              'Disease',
              'Specimen Type',
              'Requesting Physicians First Name',
              'Requesting Physicians Last Name',
              'Accession Date',
              'Collection Date',
              'Received Date']


def keep_new_logs(directory, minutes=2):
    '''removes older than specified minutes in a directory'''
    for file in os.listdir(directory):
        if 'pending' in file and file.endswith('csv'):
            log_path = os.path.join(directory, file)
            time_diff = datetime.now() - timedelta(minutes=minutes)
            log_time = datetime.fromtimestamp(os.path.getctime(log_path))

            if log_time < time_diff:
                try:
                    os.remove(log_path)
                    print(f"Removed: {file}")
                except OSError as e:
                    print(f"Not Removed: {e}")
                    pass


# create new log with timestamp
mye_log = os.path.join(S_LOGS, 'ngs_log.xls')
df = pd.read_excel(mye_log)
df.rename(columns=COL_RENAME, inplace=True)
df = df.filter(COL_FILTER)
log_name = f'pending_{datetime.now().strftime("%m.%d.%Y_%H.%M")}.csv'
log_path = os.path.join(NGS_MYE, log_name)
df.to_csv(log_path, index=False)
print(f"Created: {log_name}")

# remove old logs
keep_new_logs(NGS_MYE, minutes=10)
