#!/home/sbsuser/venv/bin/python3.11
import csv
import json
import os
import pandas as pd
from sqlalchemy import INTEGER, DATE
from utils.global_vars import COMPLETE_JSON, MYE_DB, TEMP_ID, S_DRIVE
from utils.mnt_win import mount_drive
from utils.sql_con import sql_con


def retrieve_case_details():
    """
    Retrieve case details from JSON files and write to a temporary CSV file.
    """
    with open(TEMP_ID, 'w') as case_details:
        wr = csv.writer(case_details)
        wr.writerow(['CaseID',
                     'Accession',
                     'MRN',
                     'DateOfBirth',
                     'FirstName',
                     'LastName',
                     'OrderingPhysician',
                     'Identified',
                     'SpecimenType',
                     'SampleType',
                     'DateCollected',
                     'DateReceived',
                     'DateAccessioned',
                     'DateCreated',
                     'Panel',
                     'Indication',
                     'DISEASE'])

        for file in os.listdir(COMPLETE_JSON):
            json_path = os.path.join(COMPLETE_JSON, file)
            with open(json_path) as json_file:
                data = json.load(json_file)
                sp = data['specimens'][0]
                accession = sp['accessionNumber']
                phy = data.get('physicians', [{}])[0]
                mr = sp.get('medicalRecordNumbers', [{}])[0]
                wr.writerow([
                    data['id'],
                    accession,
                    mr.get('mrn', ''),
                    sp.get('dateOfBirth', ''),
                    sp.get('firstName', ''),
                    sp.get('lastName', ''),
                    f"{phy.get('firstName', '')} {phy.get('lastName', '')}".strip(),
                    data['identified'],
                    sp['type']['label'],
                    data['sampleType'],
                    sp['datecollected'].split('T')[0],
                    sp['dateReceived'].split('T')[0],
                    sp['dateAccessioned'].split('T')[0],
                    data['dateCreated'],
                    data['dagName'].split('_')[-1],
                    data['indication'],
                    data['disease']['label']])


def update_cgw_case_details():
    """
    Update case_details table in the MySQL db with case details.
    """

    # cgw cases and informatics jobs left join
    df = pd.read_csv(TEMP_ID)
    df.sort_values(by=['DateCreated', 'CaseID'], inplace=True)
    df.drop_duplicates(inplace=True)

    # send to MySQL table CGW_ID, all cases with their job IDs
    with sql_con(MYE_DB).connect() as db_con:
        df.to_sql('case_details', db_con, if_exists='replace', index=False,
                  dtype={'CaseID': INTEGER,
                         'DateOfBirth': DATE,
                         'DateCollected': DATE,
                         'DateReceived': DATE,
                         'DateAccessioned': DATE,
                         'DateCreated': DATE})

        os.remove(TEMP_ID)
        print(f'INFO: case_details table updated')


if __name__ == "__main__":
    mount_drive(S_DRIVE)

    # Download case details JSONs of new cases
    retrieve_case_details()
    update_cgw_case_details()
    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
