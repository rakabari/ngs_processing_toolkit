#!/home/sbsuser/venv/bin/python3.11
import xml.etree.ElementTree as ET
import xmltodict
import os
import pandas as pd
from typing import List
from datetime import datetime
from interop import py_interop_run_metrics, py_interop_summary
from utils.sql_con import sql_con, get_distinct_values, drop_sort
from utils.run_validation import is_valid_run, is_b2f_complete
from utils.global_vars import S_DRIVE, NGSDATA
from utils.mnt_win import mount_drive
from sav_variables import *


def remove_col_spaces(df):
    '''repace space with undersocre in column names'''
    df.columns = df.columns.str.replace(' ', '_')
    return df


def lower_col(df):
    '''renames columns to lowercase'''
    df.columns = df.columns.str.lower()
    return df


def instrument_id(df: pd.DataFrame, df_trps: pd.DataFrame) -> None:
    """
    Add the instrument serial number to the DataFrame.
    Different tags for miseq & nextseq
    """
    try:
        df['Instrument_SN'] = df_trps['scannerid']
    except KeyError:
        df['Instrument_SN'] = df_trps['instrumentid']


def sn_pn_date(df: pd.DataFrame, df_trps: pd.DataFrame, key: str) -> None:
    """
    Add the serial number, part number and expiry date to the DataFrame.
    """
    df_frt = pd.json_normalize(df_trps[key])
    kw = key.replace('rfidtag', '').upper()
    lower_col(df_frt)
    df[f'{kw}_SerialNo'] = df_frt.get(['serialnumber'], '')
    df[f'{kw}_PartNo'] = df_frt.get(['partnumber'], '')
    df[f'{kw}_Expiry'] = pd.to_datetime(
        df_frt['expirationdate'], errors='coerce')


def software_version(df: pd.DataFrame, df_trps: dict, key: str) -> None:
    """
    Add the software name and version (miseq/nextseq) to the DataFrame.
    """
    df_su = pd.json_normalize(df_trps[key])
    lower_col(df_su)
    df['Software'] = df_su.get(['applicationname'], '')
    df['Software_Ver'] = df_su.get(['applicationversion'], '')


def run_identifier(rfpath: str, key: str) -> bool:
    """
    Identify the NGS panel using the samplesheet file.
    """
    for file in os.listdir(rfpath):
        if 'samplesheet' in file.lower() and file.endswith('csv'):
            with open(os.path.join(rfpath, file), 'r') as ss:
                if key in ss.read().lower():
                    return True


def panel_identifier(rfpath: str) -> str:
    """
    Identify NGS panel using run_identifier function
    """
    if run_identifier(rfpath, 'myeloid'):
        return 'Myeloid'
    if run_identifier(rfpath, 'cftr'):
        return 'CF'
    if run_identifier(rfpath, 'exome'):
        return 'WES'


def intrument_type(rf: str) -> str:
    """
    Extract the instrument type from the run ID.
    """
    instr = rf.split('_')[1]
    if instr.startswith('M'):
        return 'MiSeq'
    if instr.startswith('N'):
        return 'NextSeq'


def run_date(rf) -> datetime.date:
    """
    Extract the run date from the run ID.
    """
    d1 = rf.split('_')[0]
    d2 = f'20{d1[:2]}-{d1[2:4]}-{d1[4:6]}'
    d3 = datetime.strptime(d2, '%Y-%m-%d').date()
    return d3


def run_params(rfpath: str) -> pd.DataFrame:
    """
    Extract run parameters including RunID, RunName, Panel, Instrument,
    RunDate, RunNumber, RTAVersion, InstrumentID, FlowcellSerialNumber,
    FlowcellPartNumber, FlowcellManufactureDate, PR2BottleSerialNumber,
    PR2BottlePartNumber, PR2BottleManufactureDate, ReagentKitSerialNumber,
    ReagentKitPartNumber, ReagentKitExpirationDate, SoftwareVersion.
    """

    ####### RUN_PARAMETERS LOTS #######
    rf = rfpath.split('/')[-1]
    rp_xml = os.path.join(rfpath, 'RunParameters.xml')

    # Extract required information from the XML dictionary
    tree = ET.parse(rp_xml)
    xml_data = tree.getroot()
    xmlstr = ET.tostring(xml_data, encoding='utf8', method='xml')
    data_dict = dict(xmltodict.parse(xmlstr))

    # Construct a dataframe to store the run parameters
    df_rt = pd.DataFrame()
    df_trps = pd.DataFrame(data_dict).T
    df_trps.reset_index(inplace=True)
    lower_col(df_trps)
    df_rt['RunID'] = df_trps['runid']

    try:
        df_rt['RunName'] = str([s for s in df_trps['experimentname']][0])
    except KeyError:
        df_rt['RunName'] = "NA"

    df_rt['Panel'] = panel_identifier(rfpath)
    df_rt['Instrument'] = intrument_type(rf)
    df_rt['RunDate'] = run_date(rf)

    df_rt['RunNumber'] = df_trps['runnumber']
    df_rt['RTAVersion'] = df_trps['rtaversion']

    instrument_id(df_rt, df_trps)
    sn_pn_date(df_rt, df_trps, 'flowcellrfidtag')
    sn_pn_date(df_rt, df_trps, 'pr2bottlerfidtag')
    sn_pn_date(df_rt, df_trps, 'reagentkitrfidtag')
    software_version(df_rt, df_trps, 'setup')
    return df_rt


def id_name_panel(df: pd.DataFrame, rfpath: str) -> pd.DataFrame:
    """
    Insert run ID, name, panel, instrument, and run date columns into a Pandas DataFrame in order.
    """
    # Get run parameters
    params = run_params(rfpath)

    # Insert columns into DataFrame
    df.insert(0, 'RunID', params['RunID'].values[0])
    df.insert(1, 'RunName', params['RunName'].values[0])
    df.insert(2, 'Panel', params['Panel'].values[0])
    df.insert(3, 'Instrument', params['Instrument'].values[0])
    df.insert(4, 'RunDate', params['RunDate'].values[0])

    return df


def index_per_sample(rfpath: str) -> pd.DataFrame:
    """
    Extract index information from sequencing run metrics.
    """

    ####### READS_INDEXING PER SAMPLE #######
    metrics = py_interop_run_metrics.run_metrics()
    run_folder = metrics.read(rfpath)
    sum_index = py_interop_summary.index_flowcell_summary()
    py_interop_summary.summarize_index_metrics(metrics, sum_index)

    sum_l = sum_index.at(0)
    d_index = []
    for label, func in COL_INDEX:
        d_index.append((label, pd.Series([getattr(sum_l.at(i), func)() for i in range(
            sum_l.size())], index=[sum_l.at(i).id() for i in range(sum_l.size())])))

    ix = pd.DataFrame.from_dict(dict(d_index)).round(2)
    ix = id_name_panel(ix, rfpath)
    remove_col_spaces(ix)
    return ix


def read_transpose(rd: pd.DataFrame, lj: pd.DataFrame, field: str) -> None:
    """
    Extracts series from ls df and adds to rd df.
    The field is to extracted from lj DataFrame.
    """

    rd[f'{field}_R1'] = lj.loc['Read 1', field].round(2)
    rd[f'{field}_R2'] = lj.loc['Read 2', field].round(2)
    rd[f'{field}_R3'] = lj.loc['Read 3', field].round(2)
    rd[f'{field}_R4'] = lj.loc['Read 4', field].round(2)
    rd[f'{field}_Non-Indexed'] = lj.loc['Non-Indexed Total', field].round(2)
    rd[f'{field}_Total'] = lj.loc['Total', field].round(2)


def value_mean(val):
    """
    Calculates the mean of the input value if it has a mean attribute, 
    otherwise the value itself.
    """
    return val.mean() if hasattr(val, 'mean') else val


def run_summary(rfpath: str) -> pd.DataFrame:
    """   
    Summarize and format SAV metrics data for a sequencing run
    """

    ####### RUN SUMMARY #######
    # Create a new run metrics object and read the sequencing run data
    metrics = py_interop_run_metrics.run_metrics()
    run_folder = metrics.read(rfpath)

    # Create a new run summary object and summarize the run metrics
    sum_run = py_interop_summary.run_summary()
    py_interop_summary.summarize_run_metrics(metrics, sum_run)

    # Create a list of tuples for row summaries
    row_sum = [('Read 1', sum_run.at(0).summary()),
               ('Read 3', sum_run.at(2).summary()),
               ('Read 2', sum_run.at(1).summary()),
               ('Read 4', sum_run.at(3).summary()),
               ('Non-Indexed Total', sum_run.nonindex_summary()),
               ('Total', sum_run.total_summary())]

    # Compute summary statistics for each column
    d_sum = []
    for label, func in COL_SUM1:
        d_sum.append((label, pd.Series([getattr(r[1], func)(
        ) for r in row_sum], index=[r[0] for r in row_sum])))

    # Create a new DataFrame from the dictionary and set the index name
    s1 = pd.DataFrame.from_dict(dict(d_sum))
    s1.index.names = ['READ']

    def read_info(n, l=[]):
        '''Compute read-specific information'''
        for label, func in COL_SUM2:
            l.append((label, pd.Series([value_mean(getattr(r, func)()) for r in [
                sum_run.at(n).at(s) for s in range(sum_run.lane_count())]])))
        df = pd.DataFrame.from_dict(dict(l))
        remove_col_spaces(df)
        return df

    # Compute read-specific information for all reads and concatenate the results
    s2 = pd.concat([read_info(0), read_info(1), read_info(2), read_info(3)],
                   ignore_index=True, sort=True)

    # Select the relevant columns and set the index name
    s2 = s2.iloc[:4, :7]
    s2.index = ['Read 1', 'Read 2', 'Read 3', 'Read 4']
    s2.index.names = ['READ']

    # Merge the two DataFrames based on the READ column
    lj = s1.merge(s2.rename({'READ': 'READ'}, axis=1),
                  left_on='READ', right_on='READ', how='left')

    ####### READS_TOTAL #######
    # create a new index-lane summary object and summarize the index metrics
    sum_reads = py_interop_summary.index_lane_summary()
    py_interop_summary.summarize_index_metrics(metrics, 0, sum_reads)

    # store the index metrics summary data
    d_reads = []
    for label, func in COL_READS:
        d_reads.append(
            (label, pd.Series([getattr(sum_reads, func)()], index=[1])))

    # remove spaces in the column names and create a new DataFrame from the dictionary
    remove_col_spaces(lj)
    rd = pd.DataFrame.from_dict(dict(d_reads)).round(2)

    # add new columns
    rd = id_name_panel(rd, rfpath)
    rd['Density'] = ((lj.loc[s2.index, 'Density'].mean())/1000).round(0)
    rd['PF_Percent'] = (lj.loc[s2.index, 'Percent_PF'].mean()).round(2)
    rd['Yield_Total'] = lj.loc['Total', 'Yield_Total_G'].round(2)
    rd['Percent_Aligned'] = lj.loc['Total', 'Percent_Aligned'].round(2)

    # Extracts series from ls df and adds to rd df
    read_transpose(rd, lj, 'Percent_Error_Rate')
    read_transpose(rd, lj, 'Intensity_Cycle_1')
    read_transpose(rd, lj, 'Percent_Q30')
    read_transpose(rd, lj, 'Legacy_Phasing_Rate')
    read_transpose(rd, lj, 'Legacy_Prephasing_Rate')

    rd.drop(DEL_COL, axis=1, inplace=True)
    remove_col_spaces(rd)

    return rd


def sav_metrics_to_db(db_con, rfpath_root: str):
    '''
    Sends SAV metrics tables to database.
    '''
    completed = get_distinct_values('summary', columns=['RunID'], db_con=db_con)

    for rf in os.listdir(rfpath_root):
        rfpath = os.path.join(rfpath_root, rf)
        if rf not in completed and is_valid_run(rfpath) and is_b2f_complete(rfpath, n=0):
            print(f'INFO: {rf}: b2f completed_adding to the list')

            ## RUN_PARAMETERS LOTS ##
            print(f'INFO: {rf}: Parsing Run Parameters')
            rp = run_params(rfpath)
            rp.to_sql('run_lots', db_con, if_exists='append', index=False)
            drop_sort(rp, 'run_lots', db_con,
                      drop=['RunID'], sort=['RunID'])

            ## READS_INDEXING PER SAMPLE ##
            print(f'INFO: {rf}: Parsing Read Indexing')
            ix = index_per_sample(rfpath)
            ix.to_sql('percent_index', db_con, if_exists='append', index=False)
            drop_sort(ix, 'percent_index', db_con,
                      drop=['Sample_ID', 'RunID'], sort=['RunID', 'Index_Number'])

            ## RUN SUMMARY ##
            print(f'INFO: {rf}: Parsing Run Summary')
            rs = run_summary(rfpath)
            rs.to_sql('summary', db_con, if_exists='append', index=False)
            drop_sort(rs, 'summary', db_con,
                      drop=['RunID'], sort=['RunID'])


if __name__ == '__main__':
    # Mount the drive
    mount_drive(S_DRIVE)

    try:
        with sql_con(SAV_DB).connect() as db_con:
            sav_metrics_to_db(db_con, NGSDATA)
            # sav_metrics_to_db(db_con, '/mnt/isiloncwb01_NGSData/NGS_Myeloid/Illumina_Runs/Older_Runs/')
    except Exception as e:
        print(f'ERROR: {e}')

    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
