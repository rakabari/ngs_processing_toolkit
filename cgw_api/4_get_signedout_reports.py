#!/home/sbsuser/venv/bin/python3.11
# import pypaths  # for cronjob
import os
import subprocess
from datetime import datetime
from dateutil.relativedelta import relativedelta
from api_functions import get_response, res_to_file
from utils.global_vars import API_URL, PATIENT_REPORTS


def get_completed_cases(path):
    """
    Returns a list of case IDs for all downloaded patient reports in the specified path.
    """
    return set([i.split('_')[0] for i in os.listdir(path)])


def get_signed_cases(start_date):
    """
    Returns a list of signed out cases within the date range specified.
    """
    signed_cases_url = f"{API_URL}?dateSignedOutStart={start_date.strftime('%Y-%m-%d')}"
    # signed_cases_url = f"{API_URL}?dateSignedOutStart=2020-09-02&dateSignedOutEnd=2022-09-02"
    signed_cases = get_response(signed_cases_url).json()
    return signed_cases


def download_report(case_id, accession, report_id, output_dir, report_format):
    """
    Downloads a report in the specified format for a given case, accession, and report ID.
    """
    # Construct the URL and output file paths based on the input parameters
    url = f'{API_URL}{case_id}/reports/{report_id}?format={report_format}'
    ids = f"{case_id}_{accession}_{report_id}"
    output_file = f'{output_dir}/{ids}_report.{report_format}.gz'

    # Download the report and save it to the specified output file
    response = get_response(url)
    res_to_file(response, output_file)

    # Decompress the output
    subprocess.run(f'gunzip {output_file}', shell=True, check=True)

    # Log a message indicating that the report was downloaded
    print(f'INFO: {ids} : {report_format.upper()} report downloaded')


def download_recent_reports(output_dir):
    """
    Downloads the most recent PDF and JSON reports for each signed out case that has not already been downloaded.
    """
    completed = get_completed_cases(output_dir)
    start_date = datetime.today() - relativedelta(months=1)  # (today-1 month)
    signed_cases = get_signed_cases(start_date)

    for i in signed_cases:  # to check against all CGW signedout cases
        case_id = str(i['id'])
        accession = str(i['accessionNumber'])
        if case_id not in completed:  # skip downloaded cases
            case_url = f'{API_URL}{case_id}'
            case = get_response(case_url).json()

            # Download only the most recent report (greatest id)
            report_ids = []
            if 'reports' in case.keys():
                for report in case['reports']:
                    if report['signedOut'] == True:
                        report_ids.append(int(report['id']))
            report_id = str(max(report_ids))
            download_report(case_id, accession, report_id, output_dir, 'json')
            download_report(case_id, accession, report_id, output_dir, 'pdf')


if __name__ == '__main__':
    try:
        download_recent_reports(PATIENT_REPORTS)
    except Exception as e:
        print(f'INFO: {e}')
        pass
    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
