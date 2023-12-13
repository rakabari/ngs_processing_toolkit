#!/home/sbsuser/venv/bin/python3.11
# import pypaths  # for cronjob
# Standard library imports
import os
import subprocess
from datetime import datetime

# Local application/library specific imports
from utils.global_vars import AWS_CRED, FM_CREDS, S_DRIVE, S3_PATH
from utils.mnt_win import mount_drive


def get_newest_credential_file(s3data: str):
    """
    Returns the file with the most recent date in the filename 
    when there are multiple credential files in the directory
    """
    dictionary = {}
    for file in os.listdir(s3data):
        if 'credentials' in file:
            date_str = file.split(
                '_')[-1].split('.txt')[0].replace('.', '/')
            date = datetime.strptime(date_str, "%m/%d/%Y")
            dictionary[os.path.join(s3data, file)] = date
    return max(dictionary, key=dictionary.get)


def update_aws_credentials(new_creds_path: str, old_creds_path: str):
    """
    Updates AWS credentials if current credentials are older than 90 days.
    """
    with open(new_creds_path, 'r') as new_cred_file:
        new_creds = new_cred_file.readlines() + ['\n']

    with open(old_creds_path, 'r') as old_cred_file:
        old_creds = old_cred_file.readlines()

    new_access_key = new_creds[0]
    new_secret_key = new_creds[1]

    if old_creds[4] == new_access_key and old_creds[5] == new_secret_key:
        print('INFO: AWS credentials not to be updated')
    else:
        old_creds[4] = new_access_key
        old_creds[5] = new_secret_key

        with open(old_creds_path, 'w') as old_cred_file:
            old_cred_file.writelines(old_creds)

        print('INFO: AWS credentials updated')


def s3_sync(s3data: str, s3_cred: str):
    """Main function that syncs data from S3 to the mounted S_DRIVE."""
    aws_cli = '/usr/local/bin/aws'
    sync_cmd = f'{aws_cli} s3 sync --profile {s3_cred} s3://integration-prod-upstateny-ae1/ {s3data}'
    subprocess.run(sync_cmd, shell=True, check=True)


if __name__ == '__main__':
    try:
        mount_drive(S_DRIVE)
        update_aws_credentials(get_newest_credential_file(S3_PATH), AWS_CRED)
        s3_sync(S3_PATH, FM_CREDS)
    except Exception as e:
        print(f'Error: {e}')

    print(f'INFO: Completed: {os.path.basename(__file__)}\n')

# ORD-0810964-01.xml removed
