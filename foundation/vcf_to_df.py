#!/home/sbsuser/venv/bin/python3.11
import io
import os
import pandas as pd
import shutil
from utils.global_vars import REJECT_PATH


def str_to_dict(string):
    """
    Convert a semicolon-delimited string of key-value pairs into a dictionary.
    """
    return {k: v for k, v in (kv.split('=', 1) for kv in string.split(';') if '=' in kv)}


def process_info_column(df):
    # If not empty, process the INFO column using str_to_dict function

    df['INFO'] = df['INFO'].apply(str_to_dict)

    # Normalize the INFO column and join with the DataFrame
    df = df.join(pd.json_normalize(df['INFO']))

    # Drop unwanted columns
    df.drop(df.columns[0:8], axis=1, inplace=True)

    # Convert af and depth columns to float and int types
    df['VAF'] = (df['af'].astype(float)*100).round(2)
    df['Depth'] = df['depth'].astype(int)

    # Rename columns
    df = df.rename(columns={'gene_name': 'Gene',
                            'transcript_name': 'Transcript',
                            'cosmic_status': 'COSMIC',
                            'effect': 'EFFECT'})

    # Create HGVSc and HGVSp columns
    df['HGVSc'] = 'c.' + df['cds_syntax']
    df.replace({'HGVSc': {'c.none': ''}}, inplace=True)
    df['HGVSp'] = 'p.' + df['protein_syntax']
    df.replace({'HGVSp': {'p.none': ''}}, inplace=True)
    df['HGVSp'].replace({'p.spl': 'spl'}, regex=True, inplace=True)

    df = df.filter(['FMI_CaseID', 'Variant', 'VAF', 'Depth', 'Gene',
                    'Transcript', 'HGVSc', 'HGVSp', 'COSMIC', 'EFFECT'])
    return df


def vcf_to_df(vcf_path):
    """
    Converts a VCF file to a Pandas DataFrame.
    """

    # Get the filename and remove the extension to use as FMI_CaseID
    vcf_name = os.path.basename(vcf_path)
    file_name = os.path.splitext(vcf_name)[0]

    # Create a reject_vcf path to store empty VCF files
    reject_vcf = os.path.join(REJECT_PATH, 'vcf_empty_info')

    with open(vcf_path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]

        # Convert the remaining lines into a DataFrame, set dtype as str, and use tab as separator
        df = pd.read_csv(io.StringIO(''.join(lines)), dtype=str, sep='\t')

        # Add FMI_CaseID and Variant columns
        df['FMI_CaseID'] = file_name
        df['Variant'] = (df['#CHROM'] + ':' + df['POS'] + ':' +
                         df['REF'] + '>' + df['ALT'])

        # Fill any NaN values with empty string
        df = df.fillna('')

        if len(df['INFO'].value_counts()) > 0:
            print(f'INFO: {file_name} PROCESSING')
            df = process_info_column(df)
        else:
            # Reject file with empty INFO field
            print(f'WARN: {file_name} Not Processed Empty INFO Field')
            shutil.copy(vcf_path, os.path.join(reject_vcf, vcf_name))

    return df
