#!/home/sbsuser/venv/bin/python3.11
import os
from json_functions import json_pretty, parse_json_report
from sql_variables import patientReport_q
from utils.sql_con import sql_con, get_distinct_values, execute_sql_file
from utils.global_vars import MYE_DB, PATIENT_REPORTS


def get_files_to_process(output_dir, db_con):
    """
    Given the path to the directory containing the JSONs and a database connection object,
    returns a list of JSON files in the directory that have not been processed according to the accessions in the database.
    """
    processed = get_distinct_values(table='patient_reports',
                                    columns=['Accession'],
                                    db_con=db_con)
    
    to_be_processed = []
    for file in os.listdir(output_dir):

        # Skip test cases
        if len(file.split('_')) != 4:
            continue

        # Skip validation cases
        if not 'MD' in file:
            continue

        # Skip PDFs
        if not file.endswith('.json'):
            continue

        accession = file.split('_')[1]
        if accession not in processed:
            json_path = os.path.join(output_dir, file)
            to_be_processed.append(json_path)

    return to_be_processed


def parse_dowloaded_json(output_dir, db_con):
    """
    Parses downloaded JSON reports and sends to database.
    """
    to_be_processed = get_files_to_process(output_dir, db_con)

    for json_path in to_be_processed:
        # Parse if there were reports downloaded
        print(f"INFO: Exporting Data to SQL from: {json_path.split('/')[-1]}")
        json_pretty(json_path)
        df = parse_json_report(json_path)
        df.to_sql('patient_reports', db_con, if_exists='append', index=False)

    if len(to_be_processed) > 0:
        # Run SQL script to derive a table for dashboard
        execute_sql_file(patientReport_q, db_con)


if __name__ == '__main__':
    with sql_con(MYE_DB).connect() as db_con:
        parse_dowloaded_json(PATIENT_REPORTS, db_con)
        print(f'INFO: Completed: {os.path.basename(__file__)}\n')
