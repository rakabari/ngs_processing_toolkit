#!/home/sbsuser/venv/bin/python3.11
from datetime import datetime
from time import sleep
import os


def is_valid_run(rfpath: str) -> bool:
    '''
    Checks if the run directory has a valid instrument S/N and starts with "2".
    '''
    rf = os.path.basename(rfpath)
    valid_sn = ['70358', '70360', '550244']
    is_valid = any(sn in rf for sn in valid_sn) and rf.startswith('2')
    return is_valid and os.path.isdir(rfpath)


def is_recent_run(rfpath: str, n: int = 24) -> bool:
    '''
    Checks if the run directory was modified in the last n hours (24h default).
    '''
    now = datetime.now()
    mtime = datetime.fromtimestamp(os.path.getmtime(rfpath))
    elapsed_hours = (now - mtime).total_seconds() / 3600
    return elapsed_hours <= n and is_valid_run(rfpath)


def is_old_run(rfpath: str, n: int = 30) -> bool:
    '''
    Checks if the run directory was modified more than n days (30d default) ago.
    '''
    now = datetime.now()
    mtime = datetime.fromtimestamp(os.path.getmtime(rfpath))
    elapsed_days = (now - mtime).total_seconds() / (24 * 3600)
    return elapsed_days > n and is_valid_run(rfpath)


def is_run_complete(rfpath: str, n: int = 300) -> bool:
    '''
    Checks if the run completion files are present and if the directory stats
    change after waiting for an additional n seconds (300s = 5m default)
    '''
    complete_files = ['RTAComplete', 'CopyComplete']
    # RTAComplete for MiSeq & CopyComplete for NextSeq run completion
    for file_name in os.listdir(rfpath):
        if any(cf in file_name for cf in complete_files):
            initial_stats = os.stat(rfpath)
            sleep(n)  # extra 5m(300s) for post-run updating
            final_stats = os.stat(rfpath)
            return initial_stats == final_stats


def is_b2f_complete(rfpath: str, n: int = 20) -> bool:
    '''
    Checks if bcl to fastq has completed by comparing the size of 
    an undetermined R1 fastq file before and after waiting for n seconds.
    '''
    for root, _, files in os.walk(rfpath):
        for file in files:
            if 'Undetermined' in file and 'R1' in file:  # unique file in all runs
                fastq_path = os.path.join(root, file)
                initial_size = os.stat(fastq_path).st_size
                sleep(n)  # check if the fastqs are still updating (20s)
                final_size = os.stat(fastq_path).st_size
                return initial_size == final_size


def run_identifier(rfpath: str, key: str) -> bool:
    '''
    Uses the sample sheet file in the run directory to identify the panel 
    by matching a given keyword (panel_name) with the contents of the file.
    '''
    for file_name in os.listdir(rfpath):
        if 'samplesheet' in file_name.lower() and file_name.endswith('.csv'):
            with open(os.path.join(rfpath, file_name), 'r') as ss_file:
                return key.lower() in ss_file.read().lower()
