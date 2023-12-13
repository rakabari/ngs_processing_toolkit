#!/home/sbsuser/venv/bin/python3.11
# import pypaths  # for cronjob
import csv
import json
import os
import pandas as pd
from sqlalchemy import INTEGER, DATE
from utils.global_vars import COMPLETE_JSON, MYE_DB, TEMP_ID
from utils.sql_con import sql_con


def retrieve_run_ids():
    """
    Retrieve run ids from JSON files and write to a temporary CSV file.
    """

    with open(TEMP_ID, 'w') as cgw_ids:
        wr = csv.writer(cgw_ids)
        wr.writerow(['CaseID',
                     'Accession',
                     'DateCreated',
                     'InfoID',
                     'Barcode',
                     'RunID'])
        for file in os.listdir(COMPLETE_JSON):
            json_path = os.path.join(COMPLETE_JSON, file)
            with open(json_path) as json_file:
                data = json.load(json_file)
                if 'informaticsJobs' in data.keys():
                    for ij in data['informaticsJobs']:
                        wr.writerow([
                            data['id'],
                            data['specimens'][0]['accessionNumber'],
                            data['dateCreated'],
                            int(ij['id']),
                            ij['input'][0]['sequencerRunInfos'][0]['barcode'],
                            ij['input'][0]['sequencerRunInfos'][0]['runId']])


def update_cgw_ids():
    """
    Update cgw_ids table in the MySQL db with new IDs.
    """

    # cgw cases and informatics jobs left join
    df = pd.read_csv(TEMP_ID)
    df.sort_values(by=['DateCreated', 'CaseID', 'InfoID'], inplace=True)
    df.drop_duplicates(inplace=True)

    # send to MySQL table CGW_ID, all cases with their job IDs
    with sql_con(MYE_DB).connect() as dbCon:
        df.to_sql('ids', dbCon, if_exists='replace', index=False,
                  dtype={'CaseID': INTEGER,
                         'InfoID': INTEGER,
                         'DateCreated': DATE})

        os.remove(TEMP_ID)
        print(f'INFO: cgw_ids table updated')


if __name__ == "__main__":
    # Download case details JSONs of new cases
    retrieve_run_ids()
    update_cgw_ids()
    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
