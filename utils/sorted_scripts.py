#!/home/sbsuser/venv/bin/python3.11
import os


def sorted_scripts(dir_path=os.getcwd()):
    """
    Returns a sorted list of numbered scripts.

    Args:
        dir_path (str): The directory path to search for script files. Defaults to the current working directory.

    Returns:
        list: A sorted list of script file paths.

    """
    scripts_list = []

    for file in os.listdir(dir_path):
        # Check if file name starts with a digit and ends with '.py'
        if file[0].isdigit() and file.endswith('.py'):
            # add its full path to the scripts_list
            scripts_list.append(os.path.join(dir_path, file))

    # Sort the scripts_list in alphabetical order
    sorted_scripts_list = sorted(scripts_list)

    return sorted_scripts_list
