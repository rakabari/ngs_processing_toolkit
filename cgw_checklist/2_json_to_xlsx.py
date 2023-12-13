#!/home/sbsuser/venv/bin/python3.11
# import pypaths  # for cronjob
import os
import shutil
import pandas as pd
from pandasql import sqldf
from utils.global_vars import CASE_NIRVANA, CHECKLIST_XLSX, RESULTS
from ckl_variables import ORDERED_COL
from ckl_functions import *
import xlsxwriter

# #


def move_completed_checklists(results_dir):
    """
    Moves completed checklists from the results_dir to the Completed_Checklists subdirectory.
    A checklist is considered completed if the signature cell (B2) of the checklist is not empty.
    """

    completed_dir = os.path.join(results_dir, 'Completed_Checklists')

    for file in os.listdir(results_dir):
        file_path = os.path.join(results_dir, file)

        # Process only excel files that are not currently open by a user
        if file.endswith('.xlsx') and '~' not in file:
            # Get signed out field from the excel checklist
            signed = str(pd.read_excel(file_path).iloc[1][2]).strip()

            if signed and signed != 'nan':
                destination_path = os.path.join(completed_dir, file)
                shutil.move(file_path, destination_path)
                print(f'INFO: Moved {file} to Completed_Checklists')


def get_completed_accessions(results_dir):
    """Returns a list of completed accessions from results_dir root"""

    # Ensure all completed checklists are moved to the appropriate directory
    move_completed_checklists(results_dir)

    # Use list comprehension to gather all completed accession numbers
    completed_accessions = [os.path.splitext(file)[0].split('_')[0]
                            for dirpath, dirnames, files in os.walk(results_dir)
                            for file in files
                            if file.endswith('.xlsx') and '_' in file]

    return completed_accessions


def process_checklist(xls_path):
    """Reads and processes a single checklist file."""
    signed_by = str(pd.read_excel(xls_path, nrows=2).iloc[1][2]).strip()

    if len(signed_by) > 1 and signed_by != 'nan':
        columns_needed = ['Variant', 'CGW', 'COSMIC', 'Known', 'Nearby',
                          'Google Scholar', 'Pubmed', 'NCCN FDA',
                          'Clinical Trials', 'Tier', 'Comments']

        checklist_dataframe = pd.read_excel(
            xls_path, usecols=columns_needed, skiprows=4)
        checklist_dataframe['signed_date'] = os.path.getmtime(xls_path)

        return checklist_dataframe


def clean_dataframes(dataframes):
    """Combines and cleans a list of dataframes."""
    combined_df = pd.concat(dataframes)
    combined_df.sort_values(by='signed_date', inplace=True)
    combined_df.drop_duplicates(subset='Variant', keep='last', inplace=True)
    combined_df.dropna(
        subset=['CGW', 'COSMIC', 'Tier'], how='all', inplace=True)

    return combined_df


def get_checked_variants(results_dir):
    """
    Parses through completed checklists and returns a cleaned dataframe of checked variants.

    Args:
        results_dir (str): The path to the directory containing the completed checklists.

    Returns:
        pandas.DataFrame: A cleaned dataframe containing checked variant information. The dataframe 
                          includes information about each variant's presence in various databases, 
                          its clinical tier, and any comments. The dataframe is sorted by the date 
                          each checklist was signed, with duplicates removed.
    """
    signed_checklists_dir = os.path.join(results_dir, 'Completed_Checklist')

    checked_dataframes = [
        process_checklist(os.path.join(signed_checklists_dir, file))
        for file in os.listdir(signed_checklists_dir)
        if file.endswith('.xlsx')
    ]

    return clean_dataframes(checked_dataframes)


def df_append_to_excel(df, filename):
    """
    Appends the given pandas DataFrame to an existing Excel file or creates a new one if it does not exist.
    """
    print(f'INFO: df appending to excel: {filename}')
    with pd.ExcelWriter(filename, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
        df.to_excel(writer, sheet_name="Variants", startcol=0,
                    startrow=5, header=None, index=False)


def process_nirvana_files(nirvana_path, results_dir, checklist_path) -> None:
    """
    Process Nirvana JSONs and generate checklists for variants that have not yet been completed.
    """

    completed_accessions = get_completed_accessions(results_dir)
    df_checked = get_checked_variants(results_dir)

    for file in os.listdir(nirvana_path):
        if not file.endswith('json.gz') and file.split('_')[0] in completed_accessions:
            continue

        json_path = os.path.join(nirvana_path, file)
        vcf_path = os.path.join(
            nirvana_path, file.replace('.json.gz', '.vcf'))
        print(f'INFO: JSON_to_EXCEL {file}')

        df_v = read_nirvana_vcf(vcf_path)
        df_j = json_to_df(json_path)
        final_df = pd.merge(df_v, df_j, how='left')
        final_df = sqldf(CLINVAR_Q)
        final_df = final_df.assign(**{c: '' for c in ADD_COL})
        final_df.set_index('Variant', inplace=True)
        final_df.update(df_checked.set_index('Variant'))
        final_df.reset_index(inplace=True)
        final_df = final_df.reindex(columns=ORDERED_COL)

        ckl_file = file.replace('json.gz', 'xlsx')
        ckl_path = os.path.join(results_dir, ckl_file)
        shutil.copy(checklist_path, ckl_path)

        df_append_to_excel(final_df, ckl_path)


if __name__ == '__main__':
    try:
        process_nirvana_files(CASE_NIRVANA, RESULTS, CHECKLIST_XLSX)
    except Exception as e:
        print(f'ERROR: {e}')
    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
