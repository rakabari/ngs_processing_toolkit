#!/home/sbsuser/venv/bin/python3.11
# import pypaths  # for cronjob
import io
import os
import pandas as pd
from pathlib import Path
from warnings import simplefilter
from utils.global_vars import CASE_FILES, MYE_DB
from utils.sql_con import sql_con, get_distinct_values
from vcf_variables import *


def read_vcf(path: str) -> pd.DataFrame:
    """
    Reads the VCF file at the specified path into a pandas DataFrame.
    Adds 'Accession', 'CaseID', 'InfoID', 'Variant', and 'Quality' columns.
    """
    with open(path, 'r') as f:
        # Read all lines except those starting with '##'
        lines = [l for l in f if '##' not in l]
        df = pd.read_csv(io.StringIO(''.join(lines)), dtype=str, sep='\t')

        # Extract accession, case ID, and info ID from file path and add as columns
        df['Accession'] = path.split('/')[-1].split('$')[1]
        df['CaseID'] = path.split('/')[-1].split('$')[0]
        df['InfoID'] = path.split('/')[-1].split('$')[2]

        # Combine relevant columns to create 'Variant'
        df['Variant'] = (df['#CHROM'] + ':' + df['POS'] + ':' +
                         df['REF'] + '>' + df['ALT'])

        # Renmae QUAL column
        df['Quality'] = df['QUAL']

        return df.fillna('')


def get_col_value(df: pd.DataFrame, col_key: str) -> str:
    """
    Returns the value in the specified column of the DataFrame, or an empty string if the column does not exist.
    Used for KeyError Exceptions
    """
    return df.get(col_key, '')


def add_cols_to_df(df: pd.DataFrame, df_is: pd.DataFrame, col_list: list) -> None:
    """
    Adds columns from another DataFrame to the specified DataFrame.
    Uses the column names in the given list to match columns between DataFrames.
    """
    for col in col_list:
        df[col] = get_col_value(df_is, col)


def add_no_value(s: str) -> str:
    """
    Adds '=no_value' to a string if it does not contain an '=' character.
    """
    return s + '=no_value' if '=' not in s else s


def combine_variant_data(df_is: pd.DataFrame, k: str) -> str:
    """
    Combines data from three columns in the given DataFrame into a single string.
    The column names are generated using the given string as a prefix.
    """
    vision_key = f'{k}_Vision_VariantPlex'
    freebayes_key = f'{k}_Freebayes_VariantPlex'
    lofreq_key = f'{k}_LoFreq_VariantPlex'
    return get_col_value(df_is, vision_key) + get_col_value(df_is, freebayes_key) + get_col_value(df_is, lofreq_key)


def get_unique_values(lst: str) -> str:
    """
    Returns a string of unique values in the given '|' delimited string.
    """
    try:
        return '|'.join(str(set(lst.split('|'))).split(',')).strip(
            "{}").replace("'", "").replace(" ", "").strip('|').replace('%3D', '=')
    except:
        TypeError


def csq_normalize(df_is, n):
    """
    Normalize the 'CSQ' column of the input DataFrame 'df_is' containing comma-separated values,
    each containing pipe-separated key-value pairs, and extract the values corresponding to the first 'num_values' keys.
    Returns a DataFrame with one column for each key and row for each original row in 'df_is'.
    """
    l = []
    for n in range(n):
        l.append(pd.json_normalize(df_is.apply(lambda row: dict(zip(
            CSQ_COL, row['CSQ'].split(',')[n].split('|') if row['CSQ'].count(',') >= n else row['CSQ'].split(',')[0].split('|'))), axis=1).fillna('')))
    d = l[0] + '|' + l[1] + '|' + l[2] + '|' + l[3] + '|' + l[4] + '|' +\
        l[5] + '|' + l[6] + '|' + l[7] + '|' + l[8] + '|' + l[9] + '|' +\
        l[10] + '|' + l[11] + '|' + l[12] + '|' + l[13] + '|' + l[14] + '|' +\
        l[15] + '|' + l[16] + '|' + l[17] + '|' + l[18] + '|' + l[19] + '|' +\
        l[20] + '|' + l[21] + '|' + l[22] + '|' + l[23] + '|' + l[24] + '|' +\
        l[25] + '|' + l[26] + '|' + l[27] + '|' + l[28] + '|' + l[29] + '|' +\
        l[30] + '|' + l[31] + '|' + l[32] + '|' + l[33] + '|' + l[34]
    return d.applymap(get_unique_values)


def to_num(df_ncnv: pd.DataFrame, exclude_list: list[str]) -> pd.DataFrame:
    """
    Convert all columns in the input DataFrame 'df_ncnv' except those in 'exclude_list' to numeric values.
    """
    for col in df_ncnv.columns:
        if col not in exclude_list:
            try:
                df_ncnv[col] = pd.to_numeric(df_ncnv[col])
            except:
                ValueError
    return df_ncnv


def format_gene(SYMBOL: str) -> str:
    """
    Return the input 'SYMBOL' string if it is in the GENE_LIST, or the first valid value after splitting by '|'.
    """
    if '|' in SYMBOL:
        for i in SYMBOL.split('|'):
            if i in GENE_LIST:
                return i
    return SYMBOL


def format_gene_aa_vtype(df_ncnv: pd.DataFrame) -> None:
    """
    Replace the 'SYMBOL', 'HGVSp', and 'VARIANT_CLASS' columns of the input DataFrame 'df_ncnv'
    with cleaned versions based on the 'format_gene', 'AA', and 'VC' dictionaries respectively.
    """
    df_ncnv['SYMBOL'] = df_ncnv['SYMBOL'].apply(format_gene)
    df_ncnv['HGVSp'] = df_ncnv['HGVSp'].replace(AA, regex=True)
    df_ncnv['VARIANT_CLASS'] = df_ncnv['VARIANT_CLASS'].replace(VC, regex=True)


def seq_reads(df_is: pd.DataFrame, n: int) -> pd.Series:
    """
    Extract the 'n'-th value from the 'DP4_LoFreq_VariantPlex' column of the input DataFrame 'df_is',
    or return the whole column if it has only one value.
    """
    try:
        return df_is['DP4_LoFreq_VariantPlex'].apply(
            lambda x: x.split(',')[n] if len(x.split(',')) > 1 else x)
    except KeyError:
        pass


def reads_per_strand(df: pd.DataFrame, df_is: pd.DataFrame, s: str, n: int) -> None:
    """
    Create a new column in the input DataFrame 'df' with the key 's' and set its values to
    the result of calling 'combine_key' with input DataFrame 'df_is' and key 's' after
    applying 'seq_reads' to the 'DP4_LoFreq_VariantPlex' column with index 'n'.
    """
    df_is[s+'_LoFreq_VariantPlex'] = seq_reads(df_is, n)
    df[s] = combine_variant_data(df_is, s)


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
        'unfiltered_vcf', columns=['InfoID'], db_con=db_con)

    # Difference between the two lists to get the InfoIDs that have not been exported
    return list(set(max_info_ids) - set(completed_metrics))


def get_files_to_process(case_files_path, db_con):
    """
    Given the path to the directory containing the VCFs and a list of InfoIDs to be processed,
    returns a list of the VCF files to be processed.
    """
    diff_info_ids = get_diff_info_ids(db_con)
    vcf_files = []
    for root, dirs, files in os.walk(case_files_path):
        for file in files:
            if file.endswith('.vcf'):
                info_id = int(file.split('$')[2])
                if info_id in diff_info_ids:
                    vcf_files.append(os.path.join(root, file))
    return vcf_files


def process_vcf(vcf_path, db_con):
    """
    Reads in VCF files and extracts data from them to be stored in a MySQL database.
    """
    file = Path(vcf_path).name
    print(f'INFO: VCF Processing {file}')
    df = read_vcf(vcf_path)

    # FORMAT:SAMPLE
    df['FORMAT_SAMPLE'] = df.apply(lambda row: dict(
        zip(row['FORMAT'].split(':'), row['SAMPLE'].split(':'))), axis=1)
    df_fs = pd.json_normalize(df['FORMAT_SAMPLE']).fillna('')

    # Ignore PerformanceWarning
    simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

    format_col = []
    for f in FORMAT_FIELDS:
        if '_' in f:  # common names
            ff = f.split('_')[0]
            df[ff] = get_col_value(df_fs, f)
            format_col.append(ff)
        else:  # different names
            df[f] = combine_variant_data(df_fs, f)
            format_col.append(f)
    df['GL'] = df['GL'].str.replace(',', ';')

    # INFO
    df['INFO_SPLIT'] = df.apply(lambda row: dict(
        add_no_value(i).split('=') for i in row['INFO'].split(';')), axis=1)
    df_is = pd.json_normalize(df['INFO_SPLIT']).fillna('')
    df['Caller'] = get_col_value(df_is, 'calledBy').str.replace(
        'Archer_Analysis_VariantPlex_', '')

    # CNV-SV columns
    add_cols_to_df(df, df_is, CNV_SV)
    df_cnv = df[df.Caller.str.startswith('Archer')].copy(deep=True)
    to_num(df_cnv, CNV_EXCLUDE)
    df_cnv.drop(columns=DROP_COL + format_col, inplace=True)
    df_cnv.to_sql('unfiltered_cnv', db_con,
                  if_exists='append', index=False)
    # db_con.commit()

    # Extract non-CNV-SV columns
    df['HRUN'] = combine_variant_data(df_is, 'HRUN')
    for k in BULK_COMB:
        df[k] = combine_variant_data(df_is, k)
        df[k] = df[k].str.replace(',', ';')
    df['ArcherUI'] = get_col_value(
        df_is, 'Archer_UI_filter_VariantPlex')

    # RF,RR,AF,AR reads from Vision, LoFreq, Freebayes
    reads_per_strand(df, df_is, 'SRF', 0)
    reads_per_strand(df, df_is, 'SRR', 1)
    reads_per_strand(df, df_is, 'SAF', 2)
    reads_per_strand(df, df_is, 'SAR', 3)

    # VISION-FREEBAYES
    add_cols_to_df(df, df_is, VISION)
    add_cols_to_df(df, df_is, FREEBAYES)

    # INFO-CSQ
    df_is['CSQ'] = combine_variant_data(df_is, 'CSQ')

    # Merge dataframes
    df = df.merge(csq_normalize(df_is, 35),
                  left_index=True, right_index=True)
    df.columns = df.columns.str.strip()  # remove whitespace

    # Process and clean data
    df_ncnv = df[~df.Caller.str.startswith(
        'Archer')].copy(deep=True)
    to_num(df_ncnv, NCNV_EXCLUDE)
    format_gene_aa_vtype(df_ncnv)
    cnv_del = DROP_COL + CNV_SV
    df_ncnv.drop(columns=cnv_del, inplace=True)
    df_ncnv.to_sql('unfiltered_vcf', db_con,
                   if_exists='append', index=False)
    # db_con.commit()


def process_vcfs():
    """
    Extracts data from VCF files and stores in a MySQL database.
    """
    with sql_con(MYE_DB).connect() as db_con:
        to_be_processed = get_files_to_process(CASE_FILES, db_con)
        for vcf in to_be_processed:
            process_vcf(vcf, db_con)


if __name__ == '__main__':
    try:
        process_vcfs()
    except Exception as e:
        print(f'WARN: {e}')
        pass
    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
