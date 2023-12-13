#!/home/sbsuser/venv/bin/python3.11
import os
import subprocess


def mount_drive(mnt_path: str) -> None:
    """Mounts the drive using the configurations in /etc/fstab.

    Args:
        mnt_path (str): Path of the drive to mount.

    Returns:
        None
    """
    if len(os.listdir(mnt_path)) > 0:
        print(f'INFO: {mnt_path} is already mounted')
    else:
        try:
            print(f'INFO: {mnt_path} is not mounted: Mounting now...')
            subprocess.run(f'mount {mnt_path}', shell=True, check=True)
            if len(os.listdir(mnt_path)) > 0:
                print(f'INFO: {mnt_path} is now mounted')
        except Exception as e:
            print(f'ERRO: {e}')
