#!/home/sbsuser/venv/bin/python3.11
import os
import pandas as pd
import tabula
from utils.global_vars import CASE_FILES, MYE_DB, TMP
from utils.sql_con import sql_con, get_distinct_values


def get_max_info_id(df):
    """
    Given a dataframe, groups by Accession and CaseID and returns the maximum InfoID
    """
    grouped = df.groupby(['Accession', 'CaseID'])[
        'InfoID'].max().reset_index().dropna()
    max_info_ids = grouped['InfoID'].astype(int).tolist()
    return max_info_ids


def get_diff_info_ids(db_con):
    """
    Given a database connection, retrieves a list of InfoIDs that have not been exported previously.
    """
    # Retrieve the maximum InfoIDs for each Accession and CaseID
    df = pd.read_sql('ids', con=db_con)
    max_info_ids = get_max_info_id(df)

    # Retrieve the InfoIDs that have been exported previously
    completed_metrics = get_distinct_values(
        'qc_metrics', columns=['InfoID'], db_con=db_con)

    # Difference between the two lists to get the InfoIDs that have not been exported
    return list(set(max_info_ids) - set(completed_metrics))


def get_files_to_process(case_files_path, db_con):
    """
    Given the path to the directory containing the PDF files and a list of InfoIDs to be processed,
    returns a list of the PDF files to be processed.
    """
    pdf_files = []
    info_ids_to_process = get_diff_info_ids(db_con)
    for root, dirs, files in os.walk(case_files_path):
        for file in files:
            if file.endswith('.pdf') and 'QC_Metrics' in file:
                info_id = int(file.split('$')[2])
                if info_id in info_ids_to_process:
                    pdf_files.append(os.path.join(root, file))
    return pdf_files


def parse_qc_table(filepath: str, db_con) -> None:
    """
    Parses the QC table from a PDF file and stores the data in a MySQL database.
    """
    filename = os.path.basename(filepath)
    print(f"INFO: Processing PDF {filename.split('DNA')[0]}")

    # Convert PDF to CSV using tabula
    tmp_csv = os.path.join(TMP, f"{os.path.splitext(filename)[0]}.csv")
    tabula.convert_into(filepath, tmp_csv, pages='1', silent=True)

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(tmp_csv).T.iloc[0:2].to_csv(tmp_csv, header=False)
    df = pd.read_csv(tmp_csv)

    # Format, replace certain characters, rearrange columns
    df.columns = df.columns.str.replace('%', 'Percent').str.replace(
        'Percent positions ', '').str.replace('x unique', 'X')
    df = df.replace({'%': '', ',': ''}, regex=True)
    df.drop(columns=['Parameter'], inplace=True)

    # Extract relevant information from the file name and insert as columns
    file_parts = filename.split('$')
    df.insert(0, 'Accession', file_parts[1])
    df.insert(1, 'CaseID', file_parts[0])
    df.insert(2, 'InfoID', file_parts[2])
    df.insert(3, 'RunID', file_parts[3])
    df = df.apply(pd.to_numeric, errors='ignore')

    # Store the DataFrame in the MySQL database
    df.to_sql('qc_metrics', db_con, if_exists='append', index=False)
    db_con.commit()
    
    # Remove the temporary CSV file
    os.remove(tmp_csv)


def process_qc_metrics():
    """
    Extracts data from PDF files and stores in a MySQL database.
    """
    with sql_con(MYE_DB).connect() as db_con:
        to_be_processed = get_files_to_process(CASE_FILES, db_con)
        for pdf in to_be_processed:
            parse_qc_table(pdf, db_con)


if __name__ == '__main__':
    try:
        process_qc_metrics()
    except Exception as e:
        print(f'WARN: {e}')
        pass
    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
