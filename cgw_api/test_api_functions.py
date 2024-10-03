#!/home/sbsuser/venv/bin/python3.11
import json
import os
import requests
import sys
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils.global_vars import CGW

API_URL = 'https://app.pieriandx.com/cgw-api/v2.0.0/case/'
TOKEN_REFRESH_URL = 'https://app.pieriandx.com/cgw-api/v2.0.0/refreshToken'
LOGIN_URL = 'https://app.pieriandx.com/cgw-api/v2.0.0/login'

def login_and_get_token() -> str:
    """Log in to the API and return the JWT token"""
    try:
        response = requests.get(LOGIN_URL, headers=CGW)
        if response.status_code == 200:
            token = response.headers['X-Auth-Token']
            return token
        else:
            print(f"Failed to log in, status code: {response.status_code}")
            sys.exit()
    except Exception as e:
        print(f'ERROR during login: {e}')
        sys.exit()

# def refresh_token(current_token: str) -> str:
#     """Refresh the JWT token"""
#     headers = CGW.copy()  # Copy the original headers
#     headers['X-Auth-Token'] = current_token  # Add the current token to the headers
#     try:
#         response = requests.get(TOKEN_REFRESH_URL, headers=headers)
#         if response.status_code == 200:
#             new_token = response.headers['X-Auth-Token']
#             return new_token
#         else:
#             print(f"Failed to refresh token, status code: {response.status_code}")
#             sys.exit()
#     except Exception as e:
#         print(f'ERROR during token refresh: {e}')
#         sys.exit()

def get_response(url: str) -> requests.Response:
    """Returns a response object from the given url using JWT for authentication."""
    headers = CGW.copy() # to avoid modifying it directly
    headers.pop('X-Auth-Key', None)  # to avoid KeyError if 'X-Auth-Key' is not found
    headers['X-Auth-Token'] = login_and_get_token() # Add 'X-Auth-Token'   
    try:
        response = requests.get(url, headers=headers, timeout=None)
        return response
    except Exception as e:
        print(f'ERROR: {e}')
        sys.exit()   

def get_cases_by_days(days: int):
    """
    Get all CGW cases within the range specified (today-60 days)
    """
    start_date = datetime.today() - relativedelta(days=days)
    start_date_str = start_date.strftime('%Y-%m-%d')  # Format change
    today_str = datetime.today().strftime('%Y-%m-%d')
    date_range = f'dateCreatedStart={start_date_str}&dateCreatedEnd={today_str}'
    return get_response(f"{API_URL}?{date_range}").json()

print(get_cases_by_days(30))
