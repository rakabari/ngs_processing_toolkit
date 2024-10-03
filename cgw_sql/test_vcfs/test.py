#!/home/sbsuser/venv/bin/python3.11
import io
import os
import pandas as pd

# Use this script when API is not working.
# Download the VCF files from CGW and places them in this directory
# The script will create TSV which can be renamed (including header).

def read_vcf(path: str) -> pd.DataFrame:
    """
    Reads the VCF file at the specified path into a pandas DataFrame.
    Adds 'Accession', 'CaseID', 'InfoID', 'Variant', and 'Quality' columns.
    """
    with open(path, 'r') as f:
        # Read all lines except those starting with '##'
        lines = [l for l in f if '##' not in l]
        df = pd.read_csv(io.StringIO(''.join(lines)), dtype=str, sep='\t')

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
    vcfs = '/home/sbsuser/scripts/cgw_sql/test_vcfs'
    for vcf in os.listdir(vcfs):
        if vcf.endswith('.vcf'):
            vcf_path = os.path.join(vcfs, vcf)
            try:
                print(f'INFO: Exporting {vcf}')
                df = get_vaf(vcf_path)
                df.columns = ['Variant', 'VAF']
                df.to_csv(f"{vcf.split('.')[0]}.tsv", sep='\t', index=False)
            except Exception as ex:
                print(f'ERROR: {ex}')
                pass
                
if __name__ == '__main__':
    process_vcf_files()
    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
