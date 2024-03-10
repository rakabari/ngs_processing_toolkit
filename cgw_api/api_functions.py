#!/home/sbsuser/venv/bin/python3.11
import json
import requests
import sys
import time
from utils.global_vars import CGW


def get_response(url: str) -> requests.Response:
    """Returns a response object from the given url"""
    try:
        response = requests.get(url, headers=CGW, timeout=None)
        while response.status_code != 200:
            response = requests.get(url, headers=CGW, timeout=None)
            print(f'{response.status_code} : Sleeping')
            time.sleep(4)
        return response
    except Exception as e:
        print(f'ERROR: {e}')
        sys.exit()


def res_to_json(response_json, filepath: str) -> None:
    """Writes the response to a JSON file (indented)"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(response_json, f, ensure_ascii=False, indent=4)


def res_to_file(response: requests.Response, filepath: str) -> None:
    """Writes the response content to a file (txt, vcf, pdf etc)"""
    with open(filepath, 'wb') as f:
        f.write(response.content)
