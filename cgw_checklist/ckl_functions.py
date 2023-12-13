#!/home/sbsuser/venv/bin/python3.11
import io
import gzip
import json
import numpy as np
import pandas as pd
from pandasql import sqldf
from warnings import simplefilter
from ckl_variables import *


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


def json_to_df(json_path):
    """
    Reads a JSON file and converts it to a Pandas DataFrame.

    Parameters:
    json_path (str): Path to the JSON file to read.

    Returns:
    Pandas DataFrame: A DataFrame containing the data from the JSON file.
    """
    header = ""
    positions = []

    # Flags to keep track of which part of the file is being read
    is_header_line = True
    is_position_line = False
    is_gene_line = False

    # Strings used to identify different parts of the file
    gene_section_line = '],"genes":['
    end_line = "]}"

    # Read the JSON file
    with gzip.open(json_path, "rt") as f:
        position_count = 0
        gene_count = 0

        for line in f:  # Loop through each line in the file
            trim_line = line.strip()  # Remove leading/trailing whitespace

            if is_header_line:
                # Only keep the header
                header = trim_line[10:-14]
                is_header_line = False
                is_position_line = True
                continue

            if trim_line == gene_section_line:
                # Start reading the gene data
                is_gene_line = True
                is_position_line = False
                continue

            elif trim_line == end_line:
                # End of the file
                break

            else:
                if is_position_line:
                    # remove any trailing ','
                    positions.append(trim_line.rstrip(','))
                    position_count += 1

    # Create an empty dictionary to store the data
    v_data = {'Variant': [],
              'dbSNP': [],
              'gnomAD': [],
              'AG_score': [],
              'AL_score': [],
              'DG_score': [],
              'DL_score': [],
              'AG_pos': [],
              'AL_pos': [],
              'DG_pos': [],
              'DL_pos': [],
              'ClinVar': []}

    # Loop through each position in the JSON file
    for position in positions:
        # Parse the position data from the JSON string
        pos_dict = json.loads(position)

        # Loop through each variant for this position
        for var_dict in pos_dict.get('variants', []):
            g_af = var_dict.get('gnomad', {})
            s_ai = var_dict.get('spliceAI', [{}])

        clin_sig = []
        clin_dis = []
        for clin_dict in var_dict.get('clinvar', {}):
            if clin_dict.get('isAlleleSpecific') is not None:
                clin_sig.append(clin_dict['significance'][0])
                if clin_dict.get('phenotypes') is not None:
                    clin_dis.append(
                        clin_dict['phenotypes'][0].replace(',', ' '))

        def float_pos(num):
            return np.format_float_positional(num, trim='-')

        # samples = pos_dict['samples'][0]

        # Add the data for this variant to the dictionary
        v_data['Variant'].append(var_dict['vid'])
        v_data['dbSNP'].append('|'.join(var_dict.get('dbsnp', '')))
        v_data['gnomAD'].append(g_af.get('allAf', ''))
        # v_data['gnomAD'].append(float_pos((g_af.get('allAf', np.NaN))))
        v_data['AG_score'].append(s_ai[0].get('acceptorGainScore', None))
        v_data['AL_score'].append(s_ai[0].get('acceptorLossScore', None))
        v_data['DG_score'].append(s_ai[0].get('donorGainScore', None))
        v_data['DL_score'].append(s_ai[0].get('donorLossScore', None))
        v_data['AG_pos'].append(s_ai[0].get('acceptorGainDistance', None))
        v_data['AL_pos'].append(s_ai[0].get('acceptorLossDistance', None))
        v_data['DG_pos'].append(s_ai[0].get('donorGainDistance', None))
        v_data['DL_pos'].append(s_ai[0].get('donorLossDistance', None))
        v_data['ClinVar'].append('|'.join(set(clin_sig)))

    df = pd.DataFrame(data=v_data)
    # df['Accession'] = json_path.split('/')[-1].split('_')[0]
    return df


def read_nirvana_vcf(path):
    """
    Reads Nirvana VCF file and returns a processed DataFrame.

    Args:
        path (str): Path to the Nirvana VCF file.

    Returns:
        pandas.DataFrame: Processed DataFrame.
    """
    # read VCF file
    with open(path, 'r') as f:
        # remove meta lines starting with '##'
        lines = [l for l in f if '##' not in l]
        # read data into pandas DataFrame
        df = pd.read_csv(io.StringIO(''.join(lines)), dtype=str, sep='\t')

    # add Accession column to DataFrame
    df['Accession'] = path.split('/')[-1].split('_')[0]
    # df['CaseID'] = path.split('/')[-1].split('$')[0]
    # df['InfoID'] = path.split('/')[-1].split('$')[2]

    # create Variant column
    df['Variant'] = (df['#CHROM'].str.replace('chr', '') + '-' + df['POS'] + '-' +
                     df['REF'] + '-' + df['ALT'])

    # create FORMAT_SAMPLE column with a dictionary of key-value pairs
    df['FORMAT_SAMPLE'] = df.apply(lambda row: dict(
        zip(row['FORMAT'].split(':'), row['SAMPLE'].split(':'))), axis=1)
    # create DataFrame from FORMAT_SAMPLE column
    df_fs = pd.json_normalize(df['FORMAT_SAMPLE']).fillna('')

    # ignore PerformanceWarning
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

    # create INFO_SPLIT column with a dictionary of key-value pairs
    df['INFO_SPLIT'] = df.apply(lambda row: dict(
        add_no_value(i).split('=') for i in row['INFO'].split(';')), axis=1)
    # create DataFrame from INFO_SPLIT column
    df_is = pd.json_normalize(df['INFO_SPLIT']).fillna('')
    # extract Caller column
    df['Caller'] = get_col_value(df_is, 'calledBy').str.replace(
        'Archer_Analysis_VariantPlex_', '')

    # extract CNV-SV columns
    add_cols_to_df(df, df_is, CNV_SV)
    # create DataFrame for CNV-SV
    df_cnv = df[df.Caller.str.startswith('Archer')].copy(deep=True)
    to_num(df_cnv, CNV_EXCLUDE)
    df_cnv.drop(columns=DROP_COL + format_col, inplace=True)

    # extract non-CNV-SV columns
    df['HRUN'] = combine_variant_data(df_is, 'HRUN')
    for k in BULK_COMB:
        df[k] = combine_variant_data(df_is, k)
        df[k] = df[k].str.replace(',', ';')
    df['ArcherUI'] = get_col_value(df_is, 'Archer_UI_filter_VariantPlex')

    # extract read counts from Vision, LoFreq, Freebayes
    reads_per_strand(df, df_is, 'SRF', 0)
    reads_per_strand(df, df_is, 'SRR', 1)
    reads_per_strand(df, df_is, 'SAF', 2)
    reads_per_strand(df, df_is, 'SAR', 3)

    # Extract keys for VISION/FREEBAYES dfs to be used for later processing
    add_cols_to_df(df, df_is, VISION)
    add_cols_to_df(df, df_is, FREEBAYES)

    # Combine the values of the 'CSQ' column in df_is and assign it to a new column 'CSQ' in df_is.
    df_is['CSQ'] = combine_variant_data(df_is, 'CSQ')

    # Merge the normalized 'CSQ' column from df_is to df
    df = df.merge(csq_normalize(df_is, 35),
                  left_index=True, right_index=True)

    df.columns = df.columns.str.strip()  # remove whitespace
    df = df[~df.Caller.str.startswith('Archer')].copy(deep=True)

    # Convert columns in df to numeric values except NCNV_EXCLUDE
    to_num(df, NCNV_EXCLUDE)

    # Format gene, amino acid, and variant type columns
    format_gene_aa_vtype(df)

    # Drop columns specified in cnv_del list
    cnv_del = DROP_COL + CNV_SV
    df.drop(columns=cnv_del, inplace=True)

    def spl(x, sep, n):
        return x.split(sep)[n] if sep in x else x

    # Apply spl function to extract information & assign the results to new columns
    df['HGVSc'] = df['HGVSc'].apply(lambda x: spl(spl(x, '|', 0), ':', 1))
    df['HGVSp'] = df['HGVSp'].apply(lambda x: spl(spl(x, '|', 0), ':', 1))
    df['rsID'] = df['Existing_variation'].apply(lambda x: spl(x, '&', 0))
    df['PolyPhen'] = df['PolyPhen'].apply(lambda x: spl(x, '|', 0))
    df['SIFT'] = df['SIFT'].apply(lambda x: spl(x, '|', 0))

    # Rename column
    df['Gene'] = df['SYMBOL']

    # Add empty columns for data entry
    df['CGW'] = ''
    df['COSMIC'] = ''

    # Apply sqldf function to dataframes
    rv_snv = sqldf(RV_SNV)
    rv_indel = sqldf(RV_INDEL)
    rv_hrun = sqldf(RV_HRUN)
    rv_sfr = sqldf(RV_SFR)
    vr_snv = sqldf(VR_SNV)
    vr_indel = sqldf(VR_INDEL)
    sv_cov = sqldf(SV_COV)

    # Concatenate all dataframes in all_dfs list and filter columns using XL_COL list.
    # Assign the result to final_df and return it.
    all_dfs = [rv_snv, rv_indel, rv_hrun, rv_sfr, vr_snv, vr_indel, sv_cov]
    final_df = pd.concat(all_dfs)
    final_df = final_df.filter(XL_COL)

    return final_df
