#!/home/sbsuser/venv/bin/python3.11
import json
import os
import shutil
from typing import List
from api_functions import get_response, res_to_file
from utils.global_vars import API_URL, AF, CASE_FILES, COMPLETE_JSON


def get_completed_cases() -> List[str]:
    """
    Get a list of completed case info_ids from the destination directory.
    """
    return [i.split('_')[2] for i in os.listdir(CASE_FILES)]


def download_case_files(json_path: str, completed: List[str]) -> None:
    """
    Download non-BAM files associated with a case and 
    save them in a subdirectory of the destination directory.

    Args:
        json_path: Path to the JSON case details file for the case.
        completed: List of completed case info_ids.
    """

    case_id, accession, info_id, *_ = os.path.basename(json_path).split('_')

    if info_id in completed:
        return

    with open(json_path) as f:
        data = json.load(f)

    for job in data['informaticsJobs']:
        if info_id != job['id']:
            continue

        out_folder = f'{case_id}_{accession}_{info_id}'
        out_dir = os.path.join(AF, out_folder)
        os.makedirs(out_dir, exist_ok=True)

        for output_file in job['output'][0]['outputFiles']:
            name = output_file['name']

            # Skip large BAM files because of the API limitations
            if name.endswith(('.bam', '.bai')):
                continue

            # Construct full path of the file for response to be written
            run_id = job['input'][0]['sequencerRunInfos'][0]['runId']
            file_name = f'{case_id}${accession}${info_id}${run_id}${name}'
            out_path = os.path.join(out_dir, file_name)

            # Construct URL for API response
            out_str = f'output/{accession}/outputFiles/{name}?compressedFile=false'
            url = f'{API_URL}{case_id}/informaticsJobs/{info_id}/{out_str}'
            response = get_response(url)

            # API response written to file
            res_to_file(response, out_path)

        print(f'INFO: CaseFiles Download_Complete {out_folder}')
        shutil.move(out_dir, os.path.join(CASE_FILES, out_folder))


if __name__ == '__main__':
    completed_cases = get_completed_cases()

    for case_json in os.listdir(COMPLETE_JSON):
        try:
            json_path = os.path.join(COMPLETE_JSON, case_json)
            download_case_files(json_path, completed_cases)
        except Exception as e:
            print(f'INFO: {e}')
            pass
    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
