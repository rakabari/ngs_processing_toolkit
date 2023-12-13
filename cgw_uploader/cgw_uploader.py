#!/home/sbsuser/venv/bin/python3.11
import boto3
import logging
import sys, os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from utils.global_vars import NGSDATA, SCRIPTS, LOGS
from utils.run_validation import is_recent_run, run_identifier, is_b2f_complete


def pierian_s3():
    """
    Returns a set of runs previously uploaded to Pierian's S3 bucket
    """
    # Load S3 credentials from application.properties
    with open('application.properties') as f:
        s3_creds = dict(line.strip().split('=')
                        for line in f if 'Key' in line)

    # Create an S3 client with the obtained credentials
    s3_client = boto3.client('s3',
                             aws_access_key_id=s3_creds['cgw.run.s3.accessKey'],
                             aws_secret_access_key=s3_creds['cgw.run.s3.secretKey'])

    # List objects in the specified S3 bucket and prefix
    response = s3_client.list_objects(
        Bucket='pdx-xfer',
        Prefix='sunyupstate/')

    # Extract the names of the runs from the S3 objects
    runs = {obj['Key'].split('/')[1] for obj in response.get('Contents', [])}

    return runs


def run_upload(rfpath):
    """
    creates and run shell command using PierianDx's java run uploader
    """
    rf = os.path.basename(rfpath)
    uploader_path = os.path.join(SCRIPTS, 'cgw_uploader')

    # Current this script's path, regardless of where it is run from
    script_path = os.path.join(uploader_path, 'uploader.py')

    # Get the script directory name from the script path
    dir_name = Path(os.path.dirname(script_path)).resolve().stem

    # Create the log directory if it doesn't already exist
    script_log_dir = os.path.join(LOGS, dir_name)
    rfpath_log_dir = os.path.join(rfpath, 'logs')
    Path(script_log_dir).mkdir(parents=True, exist_ok=True)
    Path(rfpath_log_dir).mkdir(parents=True, exist_ok=True)

    # Java command to run the uploader #
    # RunUploader-1.14.1.jar works with java-1.8.0-amazon-corretto
    java = '/usr/lib/jvm/java-1.8.0-amazon-corretto/jre/bin/java'
    java_cmd = f"{java} -jar \
        -Dloader.main=com.pdx.commandLine.ApplicationCommandLine \
        RunUploader-1.14.1.jar \
        --commandLine \
        --runFolder={rfpath} \
        --sequencer=Illumina \
        --sequencerFileType=fastq"

    # Create log name
    time_stamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    log = os.path.join(script_log_dir, f'{rf}-{time_stamp}.log')

    # Lauch Java Command from .jar path (stored in the same dir)
    os.chdir(uploader_path)
    subprocess.run(f"{java_cmd} &> {log}", shell=True, check=True)

    # Copy the log to rfpath for troubleshooting from Windows
    shutil.copy(log, rfpath_log_dir)


def is_upload_complete(rfpath):
    """
    Reads run's uploader log to check if it uploaded
    """
    rf = os.path.basename(rfpath)
    upload_logs = os.path.join(rfpath, 'logs')
    for log_name in os.listdir(upload_logs):
        if rf in log_name:
            rf_log = os.path.join(upload_logs, log_name)
            with open(rf_log, 'r') as log:
                return 'Upload completed' in log.read()


def run_uploader(rfpath: str):
    """
    Uploads a single Illumina sequencing run by checking its status
    """
    rf = os.path.basename(rfpath)

    if not is_recent_run(rfpath, n=24):
        print(f'INFO: {rf}: Run not recent or not valid')
        return

    print(f'INFO: {rf}: Run recent_Checking if it is to be uploaded...')
    if not run_identifier(rfpath, 'pierian'):
        print(f'INFO: {rf}: Run (non-pierian) not to be uploaded')
        return

    # print(f'INFO: {rf}: To be uploaded_Checking basecall conversion...')
    if not is_b2f_complete(rfpath, n=20):
        print(f'INFO: {rf}: Basecall conversion not complete')
        return

    print(f'INFO: {rf}: Basecall conversion complete_Checking S3')
    if rf in pierian_s3():
        print(f'INFO: {rf}: Run already in S3')
        return

    print(f'INFO: {rf}: Not in S3_Upload started')
    run_upload(rfpath)

    if is_upload_complete(rfpath):
        print(f'INFO: {rf}: Upload completed')
    else:
        print(f'INFO: {rf}: Upload did not complete')


def run_uploader_on_output(output_dir: str):
    """
    To be able run the uploader on a different directory
    """
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
        for rf in os.listdir(output_dir):
            run_uploader(os.path.join(output_dir, rf))
    except Exception as e:
        logging.exception(f'{e}')


if __name__ == '__main__':
    run_uploader_on_output(NGSDATA)
