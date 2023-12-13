#!/home/sbsuser/venv/bin/python3.11
# import pypaths  # for cronjob
import os
from api_functions import get_response, res_to_json
from utils.global_vars import API_URL, COMPLETE_JSON, INCOMPLETE_JSON


def get_nahg_cases(dir_path: str):
    """
    Get completed cases' info ids to skip previously downloaded JSONs
    """
    return [int(i.split('_')[-3]) for i in os.listdir(dir_path) if 'NAHG' in i]


def get_cases_by_keyword(keyword: str):
    """
    Get cgw cases (keyword:NAHG)
    """
    return get_response(f"{API_URL}?accessionNumber={keyword}").json()


def download_new_cases() -> None:
    """
    Download new cases from the CGW API within a specified range
    and save the JSON files for further analysis.
    """
    completed_cases = get_nahg_cases(COMPLETE_JSON)
    nahg_cases = get_cases_by_keyword('NAHG')

    for case in nahg_cases:
        case_id = str(case['id'])
        accession = str(case['accessionNumber'])
        idacc = f'{case_id}_{accession}'

        case_data = get_response(f'{API_URL}{case_id}').json()

        # Set file paths for success and failed cases
        failed_s = os.path.join(INCOMPLETE_JSON, idacc)
        success_s = os.path.join(COMPLETE_JSON, idacc)

        if 'reports' not in case_data or 'informaticsJobs' not in case_data:
            handle_incomplete_case(case_data, idacc, failed_s)
            continue

        info_ids = []
        for info_job in case_data['informaticsJobs']:
            info_id = int(info_job['id'])
            info_status = info_job['status']
            info_status_str = f"{info_status}_informaticsJobsStatus"
            idaccinfo = f'{idacc}_{info_id}'

            if 'outputFiles' not in info_job['output'][0]:
                # print(f"INFO: {idaccinfo}: noOutput_{info_status_str}")
                continue

            if info_status != 'complete':
                # print(f"INFO: {idaccinfo}: notComplete_{info_status_str}")
                continue

            info_ids.append(info_id)

        if max(info_ids) in completed_cases:
            print(f'INFO: {accession}: Recent Jobs already downloaded')
            continue

        info_status_str_full = f"{max(info_ids)}_{info_status_str}"
        json_path = f"{success_s}_{info_status_str_full}.json"
        res_to_json(case_data, json_path)
        print(f'INFO: Downloaded: {os.path.basename(json_path)}')


def handle_incomplete_case(case_data, idacc, failed_s):
    """
    Debugging for cases with incomplete information, gets overwritten
    """
    if 'informaticsJobs' in case_data and 'reports' not in case_data:
        status = ''
        for info_job in case_data['informaticsJobs']:
            info_id = int(info_job['id'])
            info_status = str(info_job.get('status', 'NK'))
            info_status_str = f'{info_status}_informaticsJobsStatus'
            json_path = f'{failed_s}_{info_status_str}_noReport.json'
            # res_to_json(case_data, json_path)
            status = os.path.basename(json_path)
        print(f'WARN: Not Downloaded: {status}')

    elif 'reports' in case_data and 'informaticsJobs' not in case_data:
        report_status = str(case_data['reports'][0].get('status', 'NK'))
        report_status_str = f'{report_status}_reportStatus'
        json_path = f'{failed_s}_{report_status_str}_noInfojob.json'
        # res_to_json(case_data, json_path)
        print(f'WARN: Not Downloaded: {os.path.basename(json_path)}')


if __name__ == "__main__":
    try:
        # Download case details JSONs of new cases
        download_new_cases()
    except Exception as e:
        print(f'INFO: {e}')
        pass
    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
