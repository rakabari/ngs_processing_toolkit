#!/home/sbsuser/venv/bin/python3.11
# import pypaths
import os
from utils.sorted_scripts import sorted_scripts

## Run scripts in order ##
for script in sorted_scripts(dir_path=os.path.dirname(os.path.abspath(__file__))):
    os.system(f'{script}')
