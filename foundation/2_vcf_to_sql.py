#!/home/sbsuser/venv/bin/python3.11
# import pypaths  # for cronjob
# Standard library imports
import glob
import os

# Local application/library specific imports
from utils.global_vars import FM_DB, S3_PATH, REJECT_PATH
from utils.sql_con import sql_con, get_distinct_values
from vcf_to_df import vcf_to_df


def process_vcfs(db_con):
    """Parses variants using the specified parser and sends to MySQL"""

    # get a list of vcf files to skip (previously completed/rejected)
    table = 'VCF_VARIANTS'
    completed = get_distinct_values(table, ['FMI_CaseID'], db_con)
    rejected = [file.split('.')[0] for file in os.listdir(REJECT_PATH)
                if file.endswith('.vcf')]
    skip_list = set(completed + rejected)

    # check for newly synced vcf files
    vcf_files = glob.glob(S3_PATH + '/*.vcf')
    new_vcf_files = [file for file in vcf_files
                     if file.split('/')[-1].split('.')[0] not in skip_list]

    # run vcf_parser on new files
    if new_vcf_files:
        for file_path in new_vcf_files:
            vcf_to_df(file_path).to_sql(table, db_con,
                                        if_exists='append', index=False)


if __name__ == '__main__':
    try:
        with sql_con(FM_DB).connect() as db_con:
            process_vcfs(db_con)
    except Exception as e:
        print(f'Error: {e}')

    print(f'INFO: Completed: {os.path.basename(__file__)}')
