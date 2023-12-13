#!/home/sbsuser/venv/bin/python3.11
# import pypaths  # for cronjob
import os
import pysftp
from utils.global_vars import TNX_HOST, TNX_USER, TNX_PASS, TNX_DIR, TNX_SENT, S3_PATH


def send_to_trinetx(file_path, host=TNX_HOST, user=TNX_USER, password=TNX_PASS, remote_dir=TNX_DIR):
    """Put SFTP file without hostkey and confirm if file sent"""
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # trusting the internal server

    with pysftp.Connection(host=host, username=user, password=password, cnopts=cnopts) as sftp:
        file_name = os.path.basename(file_path)
        remote_path = os.path.join(remote_dir, file_name)
        sftp.put(file_path, remote_path, confirm=False)

        # Confirm if the file is present at remote_dir
        if sftp.exists(remote_path):
            print(f'INFO: {file_name} sent to Trinetx {remote_dir}')
        else:
            print(f'INFO: {file_name} not sent to Trinetx {remote_dir}')


def send_new_xml_to_trinetx():
    """Send any new XML files in the S3 directory to Trinetx SFTP."""
    with open(TNX_SENT, 'r+') as completed_files_list:
        completed_files = {line.strip() for line in completed_files_list}

        for file in os.listdir(S3_PATH):
            if file.endswith('.xml') and file not in completed_files:
                file_path = os.path.join(S3_PATH, file)
                send_to_trinetx(file_path)
                completed_files_list.write(f'{file}\n')
                print(f'INFO: Added {file} to completed files list')


if __name__ == '__main__':
    try:
        send_new_xml_to_trinetx()
    except Exception as e:
        print(f'Error: {e}')

    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
