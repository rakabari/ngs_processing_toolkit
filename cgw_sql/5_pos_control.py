#!/home/sbsuser/venv/bin/python3.11
import io
import os
import pandas as pd
from utils.global_vars import CASE_FILES, POS, POS_BU


def completed_info_ids():
    """
    Returns a list of positive control Infomatics IDs that have been previously processed.
    """
    return [x.split('~')[-1].replace('.tsv', '') for x in os.listdir(POS_BU)]

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


def get_vaf(vcf_path):
    """
    Reads a VCF file and returns a dataframe containing the VAF values for each variant.
    """
    df = read_vcf(vcf_path)
    df['FORMAT_SAMPLE'] = df.apply(lambda row: dict(
        zip(row['FORMAT'].split(':'), row['SAMPLE'].split(':'))), axis=1)
    df_fs = pd.json_normalize(df['FORMAT_SAMPLE']).fillna('')

    # Extract VAF from the JSON-normalized DataFrame and assign it to a new column 'VAF'
    df['VAF'] = df_fs['VAF_for_report']

    # Filter out rows containing 'CNV' in the 'Variant' column
    df = df[~df['Variant'].str.contains('CNV')]

    # Filter the DataFrame to include only 'Variant' and 'VAF' columns
    df = df.filter(['Variant', 'VAF'])
    return df


def process_vcf_files():
    """
    Process VCF files in the specified directory and write results to TSV files in the specified output directories.
    """
    completed_infoids =  completed_info_ids()
    for root, dirs, files in os.walk(CASE_FILES):
        for name in files:
            if name.endswith('.vcf') and 'NAHG' in name:
                
                names = name.split('$')
                runid, infoid, accession = names[3], names[2], names[1]
                file_name = f'{runid}~{accession}~{infoid}.tsv'
                vcf_path = os.path.join(root, name)

                # if runid not in completed_runids:
                if infoid not in completed_infoids:
                    try:
                        print(f'INFO: Exporting {file_name}')

                        df = get_vaf(vcf_path)
                        df.columns = ['Variant', runid]

                        pos_tsv = os.path.join(POS, file_name)
                        df.to_csv(pos_tsv, sep='\t', index=False)

                        backup_tsv = os.path.join(POS_BU, file_name)
                        df.to_csv(backup_tsv, sep='\t', index=False)

                    except ValueError as e:
                        if 'single column format_sample' in str(e).lower():
                            print(f'ERROR: {runid}: Empty Dataframe, Possibly no variants in VCF.')
                            pass
                        else:
                            print(f'ERROR: {runid}: Other ValueError than Empty DataFrame: {e}')
                            pass
                    except Exception as ex:
                        print(f'ERROR: {runid}: {ex}')
                        pass
                    
if __name__ == '__main__':
    process_vcf_files()
    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
