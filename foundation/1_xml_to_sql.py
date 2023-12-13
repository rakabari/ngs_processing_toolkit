#!/home/sbsuser/venv/bin/python3.11
# import pypaths  # for cronjob
# Standard library imports
import glob
import os

# Local application/library specific imports
from utils.global_vars import FM_DB, FM_SQL, S3_PATH, REJECT_PATH, REJECT_BM, TEMP_PATH
from utils.sql_con import sql_con, get_distinct_values, execute_sql_file
from xml_to_df import shortvars_to_df, biomarkers_to_df


def process_xmls(xml_parser, db_con):
    """
    Parses variants using the specified parser and sends to MySQL
    """

    reject_path = REJECT_BM if xml_parser == biomarkers_to_df else REJECT_PATH
    table = 'BIOMARKERS' if xml_parser == biomarkers_to_df else 'SNV_INDEL'
    sql_file = 'derived_bm.sql' if xml_parser == biomarkers_to_df else None

    # get a list of xml files to skip (previously completed/rejected)
    completed = get_distinct_values(table, ['FMI_CaseID'], db_con)
    rejected = [file.split('.')[0] for file in os.listdir(reject_path)
                if file.endswith('.xml')]
    skip_list = set(completed + rejected)

    # check for newly synced xml files
    xml_files = glob.glob(S3_PATH + '/*.xml')
    new_xml_files = [file for file in xml_files
                     if file.split('/')[-1].split('.')[0] not in skip_list]

    # run xml_parser on new files
    if new_xml_files:
        for file_path in new_xml_files:
            xml_parser(file_path).to_sql(table, db_con,
                                         if_exists='append', index=False)

        if sql_file is not None:
            # sql files to create individual bimarker tables
            execute_sql_file(os.path.join(FM_SQL, sql_file), db_con)

    # remove temporary csv files created by xml_parser
    [os.remove(file) for file in glob.glob(os.path.join(TEMP_PATH, '*csv'))]


if __name__ == '__main__':
    try:
        with sql_con(FM_DB).connect() as db_con:
            process_xmls(shortvars_to_df, db_con)
            process_xmls(biomarkers_to_df, db_con)
    except Exception as e:
        print(f'Error: {e}')

    print(f'INFO: Completed: {os.path.basename(__file__)}')
