#!/home/sbsuser/venv/bin/python3.11
import os
import pandas as pd
import numpy as np
import datetime as dt
from utils.global_vars import POS_BU
from utils.global_vars import MYE_DB
from utils.sql_con import sql_con

variants_df = pd.read_csv('pos_control_variants.tsv', sep='\t')
merge_keys = variants_df.columns[:7].tolist()
merged_df = variants_df.copy()
tsv_files = sorted(os.listdir(POS_BU))

def process_tsv(tsv):
    tsv_path = os.path.join(POS_BU, tsv)
    tsv_df = pd.read_csv(tsv_path, sep='\t')
    filtered_df = variants_df.merge(tsv_df, on='Variant', how='left')
    if filtered_df[filtered_df.columns[-1]].isna().sum() < 30:
        return filtered_df
    return None

def aggregated_analysis(concatenated_df):
    grouped_df = concatenated_df.groupby(['Index', 'Variant', 'Variant_Type', 'Gold_Std_VF', 'Mean', '2.5_SD-', '2.5_SD+']).agg(
        VAF_Mean=('VAF', 'mean'),
        VAF_SD=('VAF', 'std'),
        VAF_Median=('VAF', 'median'),
        VAF_Min=('VAF', 'min'),
        VAF_Max=('VAF', 'max'),
    ).reset_index()
    grouped_df['VAF_2.5_SD_Lower'] = grouped_df['VAF_Mean'] - (2.5 * grouped_df['VAF_SD'])
    grouped_df['VAF_2.5_SD_Upper'] = grouped_df['VAF_Mean'] + (2.5 * grouped_df['VAF_SD'])
    numeric_columns = grouped_df.select_dtypes(include=[np.number]).columns
    grouped_df[numeric_columns] = grouped_df[numeric_columns].round(3)
    return grouped_df

for tsv in tsv_files:
    processed_df = process_tsv(tsv)
    if processed_df is not None:
        merged_df = merged_df.merge(processed_df, on=merge_keys, how='left')

# 240522_NDX550244_RUO_0031_AHC327AFX7~Training-NAHG-POOL~273143.tsv

dataframes = []
for tsv in tsv_files:
    processed_df = process_tsv(tsv)
    if processed_df is not None:
        processed_df.rename(columns={processed_df.columns[-1]: 'VAF'}, inplace=True)
        processed_df['VAF_a'] = processed_df['VAF']

        instrument_sn = tsv.split('_')[1]
        run_id = tsv.split('~')[0]
        year = int(f'20{run_id[:2]}')
        month = int(run_id[2:4])
        day = int(run_id[4:6])
        quarter = f'Q{(month-1)//3+1}'
        run_date = dt.date(year, month, day).strftime("%Y-%m-%d")

        processed_df['RunID'] = run_id
        processed_df['RunDate'] = run_date
        processed_df['Year'] = year
        processed_df['Month'] = month
        processed_df['Quarter'] =  quarter        
        processed_df['Instrument_Name'] = 'Watson' if instrument_sn == 'M70358' else ('Crick' if instrument_sn == 'M70360' else 'Darwin')
        processed_df['Instrument'] = 'MiSeq' if instrument_sn.startswith('M') else 'NextSeq'

        dataframes.append(processed_df)
concatenated_df = pd.concat(dataframes, ignore_index=True)
aggregated_df = aggregated_analysis(concatenated_df)
# concatenated_df = concatenated_df.merge(aggregated_df, on=merge_keys, how='left')


if __name__ == '__main__':
    with sql_con(MYE_DB).connect() as db_con:
        merged_df.to_sql('positive_controls_merged', db_con, if_exists='replace', index=False)
        aggregated_df.to_sql('positive_controls_aggregated', db_con, if_exists='replace', index=False)
        concatenated_df.to_sql('positive_controls_concatenated', db_con, if_exists='replace', index=False)
        print(f'INFO: Completed: {os.path.basename(__file__)}\n')