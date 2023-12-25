#!/home/sbsuser/venv/bin/python3.11
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from api_functions import get_response, res_to_json
from utils.global_vars import API_URL, COMPLETE_JSON, INCOMPLETE_JSON, S_DRIVE
from utils.mnt_win import mount_drive


def get_completed_cases(dir_path: str):
    """
    Get completed cases to skip previously downloaded JSONs
    """
    return [i.split('_')[0] for i in os.listdir(dir_path)]


def get_cases_by_days(days: int):
    """
    Get all CGW cases within the range specified (today-60 days)
    """
    start_date = datetime.today() - relativedelta(days=days)
    start_date_str = start_date.strftime('%Y-%m-%d')  # Format change
    today_str = datetime.today().strftime('%Y-%m-%d')
    date_range = f'dateCreatedStart={start_date_str}&dateCreatedEnd={today_str}'
    return get_response(f"{API_URL}?{date_range}").json()


def download_new_cases() -> None:
    """
    Download new cases from the CGW API within a specified range
    and save the JSON files for further analysis.
    """
    completed_cases = get_completed_cases(COMPLETE_JSON)
    cases_by_days = get_cases_by_days(days=30)

    for case in cases_by_days:
        case_id = str(case['id'])
        accession = str(case['accessionNumber'])
        idacc = f'{case_id}_{accession}'

        if case_id in completed_cases:
            continue

        case_data = get_response(f'{API_URL}{case_id}').json()

        # Set file paths for success and failed cases
        failed_s = os.path.join(INCOMPLETE_JSON, idacc)
        success_s = os.path.join(COMPLETE_JSON, idacc)

        if 'reports' not in case_data or 'informaticsJobs' not in case_data:
            handle_incomplete_case(case_data, idacc, failed_s)
            continue

        for info_job in case_data['informaticsJobs']:
            info_id = info_job['id']
            info_status = info_job['status']
            info_status_str = f"{info_status}_informaticsJobsStatus"
            idaccinfo = f'{idacc}_{info_id}'

            if 'outputFiles' not in info_job['output'][0]:
                print(f"INFO: {idaccinfo}: noOutput_{info_status_str}")
                continue

            if info_status != 'complete':
                print(f"INFO: {idaccinfo}: notComplete_{info_status_str}")
                continue

            info_status_str_full = f"{info_id}_{info_status_str}"
            json_path = f"{success_s}_{info_status_str_full}.json"

            # Submit the task to the executor and store the future
            res_to_json(case_data, json_path)
            print(f"INFO: {idaccinfo}: {info_status_str}")


def handle_incomplete_case(case_data, idacc, failed_s):
    """
    Debugging for cases with incomplete information, gets overwritten
    """
    if 'informaticsJobs' in case_data and 'reports' not in case_data:
        for info_job in case_data['informaticsJobs']:
            info_id = int(info_job['id'])
            info_status = str(info_job.get('status', 'NK'))
            info_status_str = f'{info_status}_informaticsJobsStatus'
            json_path = f'{failed_s}_{info_status_str}_noReport.json'
            # res_to_json(case_data, json_path)
            print(f"INFO: {idacc}_{info_id}: {info_status_str}_noReport")
    elif 'reports' in case_data and 'informaticsJobs' not in case_data:
        report_status = str(case_data['reports'][0].get('status', 'NK'))
        report_status_str = f'{report_status}_reportStatus'
        json_path = f'{failed_s}_{report_status_str}_noInfojob.json'
        # res_to_json(case_data, json_path)
        print(f'INFO: {idacc}: {report_status_str}_noInfojob')


if __name__ == "__main__":
    # Mount S Drive where the JSON responses will be written
    mount_drive(S_DRIVE)

    try:
        # Download case details JSONs of new cases
        download_new_cases()
    except Exception as e:
        print(f'INFO: {e}')
        pass
    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
