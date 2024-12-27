#!/home/sbsuser/venv/bin/python3.11
import os
import shutil
import subprocess
from pathlib import Path
from typing import List

from utils.run_validation import is_old_run
from utils.global_vars import MYE_RUNS, MYE_OLD, S_DRIVE, WATSON_DX, CRICK_DX, NGSDATA, INSTRUMENT_DRIVES
from utils.mnt_win import mount_drive


def mount_drives(mount_pints: List) -> None:
    "Mounts S and MiSeq D Drives using mount_drive function"
    for mount_point in mount_pints:
        mount_drive(mount_point)


def get_previously_transferred_runs(s_dir_list: List) -> List[str]:
    "get completed runs from S drive Myeloid Illumina_Runs"
    return [rf.name for directory in s_dir_list for rf in os.scandir(directory)]


def move_runs_to_s_drive(paths: list, s_dir_list: List) -> None:
    "Move linux share runs to S Drive"
    # list all runs on ilinux share
    linux_runs = [rf.resolve()for path in paths for rf in Path(path).iterdir()]
    already_moved = get_previously_transferred_runs(s_dir_list)

    for rf in linux_runs:
        rf = Path(rf)
        if rf.name not in already_moved and is_old_run(rf, n=30):
            print(f'INFO: Moving old run {rf} to S Drive')
            cmd = f'rsync -aq --remove-source-files {rf} {s_dir_list[0]}'
            subprocess.run(cmd, shell=True, check=True)

            # find command to remove empty source directories
            cmd_empty = f'find {rf} -type d -empty -delete'
            subprocess.run(cmd_empty, shell=True, check=True)


def remove_old_runs_from_miseqs(paths: list, s_dir_list: List) -> None:
    "Remove old MiSeq runs from D drives if they are backed up on S Drive"
    # list all runs on MiSeqOutput/MiSeqAnalysis
    miseq = [rf.resolve()for path in paths for rf in Path(path).iterdir()]
    backed_up = get_previously_transferred_runs(s_dir_list)

    for rf in miseq:
        rf = Path(rf)
        if rf.name in backed_up and is_old_run(rf, n=30):
            print(f'INFO: Removing old run {rf} from MiSeq')
            shutil.rmtree(rf)


def move_old_to_sub_dir(directory, sub_directory) -> None:
    "Move old S Drive (MiSeqRuns) runs to S Drive Older_Runs"
    for rf in os.scandir(directory):
        rf = Path(rf)
        if is_old_run(rf, n=30):
            print(f'INFO: Moving old Illumina_Runs to Older_Runs: {rf}')
            shutil.move(rf, sub_directory)


if __name__ == '__main__':
    # Mounts S and MiSeq D Drives using mount_drive function
    mount_drives([S_DRIVE, WATSON_DX, CRICK_DX])

    # Move old linux share runs to S Drive.
    move_runs_to_s_drive([NGSDATA], [MYE_RUNS, MYE_OLD])

    # Remove old MiSeq runs from D drive
    remove_old_runs_from_miseqs(INSTRUMENT_DRIVES, [MYE_RUNS, MYE_OLD])

    # Move old S Drive (Illumina_Runs) runs to S Drive Older_Runs.
    move_old_to_sub_dir(MYE_RUNS, MYE_OLD)

    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
