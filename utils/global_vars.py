#!/home/sbsuser/venv/bin/python3.11
import os

### _______________HOME where scripts are stored________________###
HOME = '/home/sbsuser'
SCRIPTS = os.path.join(HOME, 'scripts')

### _____________FULL PATHS OF SCRIPTS DIRECTORIES______________###
BCL_CONVERT_DIR = os.path.join(SCRIPTS, 'bcl_conversion')
CGW_API_DIR = os.path.join(SCRIPTS, 'cgw_api')
CGW_CHECKLIST_DIR = os.path.join(SCRIPTS, 'cgw_checklist')
CGW_SQL_DIR = os.path.join(SCRIPTS, 'cgw_sql')
CGW_UPLOADER_DIR = os.path.join(SCRIPTS, 'cgw_uploader')
FOUNDATION_DIR = os.path.join(SCRIPTS, 'foundation')
MANAGE_STORAGE_DIR = os.path.join(SCRIPTS, 'manage_storage')
SAV_DIR = os.path.join(SCRIPTS, 'sav')
LOGS = os.path.join(SCRIPTS, 'logs')
PENDING_LOGS_DIR = os.path.join(SCRIPTS, 'pending_logs')
BACKUP_DIR = os.path.join(SCRIPTS, 'backup')

SCHEDULER = os.path.join(SCRIPTS, 'scheduler')
TEMP = os.path.join(SCRIPTS, 'temp')
UTILS = os.path.join(SCRIPTS, 'utils')

### _____SCRIPTS subdirectories where SQL scripts are stored____###
FM_SQL = os.path.join(FOUNDATION_DIR, 'sql_scripts')


### ________________Full Path To Python Scripts_________________###
BCL_CONVERT = os.path.join(BCL_CONVERT_DIR, 'bcl_convert.py')
CGW_UPLOADER = os.path.join(CGW_UPLOADER_DIR, 'cgw_uploader.py')
CGW_API = os.path.join(CGW_API_DIR, 'cgw_api.py')
CGW_SQL = os.path.join(CGW_SQL_DIR, 'cgw_sql.py')
CGW_CHECKLIST = os.path.join(CGW_CHECKLIST_DIR, 'cgw_checklist.py')
FOUNDATION = os.path.join(FOUNDATION_DIR, 'foundation.py')
MANAGE_STORAGE = os.path.join(MANAGE_STORAGE_DIR, 'manage_storage.py')
SAV = os.path.join(SAV_DIR, 'sav.py')
PENDING_LOGS = os.path.join(PENDING_LOGS_DIR, 'pending_logs.py')

DAILY_BACKUP_PY = os.path.join(BACKUP_DIR, 'daily.py')
WEEKLY_BACKUP_PY = os.path.join(BACKUP_DIR, 'weekly.py')
MONTHLY_BACKUP_PY = os.path.join(BACKUP_DIR, 'monthly.py')
QUARTERLY_BACKUP_PY = os.path.join(BACKUP_DIR, 'quarterly.py')
YEARLY_BACKUP_PY = os.path.join(BACKUP_DIR, 'yearly.py')
MANUAL_BACKUP_PY = os.path.join(BACKUP_DIR, 'manual.py')


### ____________HOME where .aws/credentials is stored___________###
AWS_CRED = os.path.join(HOME, '.aws/credentials')
FM_CREDS = 'fm'  # AWS CLI profile name for foundation s3


### _______________HOME where TEMP/LOG dir stored_______________###
# LOGS = os.path.join(SCRIPTS, 'logs')
# MYELOID_TEMP = os.path.join(TEMP, 'myeloid')


### ______________Runs created by instruments here______________###
STORAGE = os.path.join(HOME, 'ngsdata')
NGSDATA = os.path.join(STORAGE, 'shared')
# NGSDATA_MOUNT = '/mnt/centos'
# NGSDATA = '/mnt/centos/home/illumina/Output'

### ___________Windows mount where analyis file stored__________###
WATSON_DX = '/mnt/watsondx'
CRICK_DX = '/mnt/crickdx'
DARWIN_RUO = '/mnt/darwinruo'
S_DRIVE = '/mnt/isiloncwb01_NGSData'
N_DRIVE = '/mnt/cpathngs_NGSData'

INSTRUMENT_DRIVES = [os.path.join(WATSON_DX, 'Illumina/MiSeqOutput'),
                     os.path.join(CRICK_DX, 'Illumina/MiSeqOutput'),
                     os.path.join(WATSON_DX,  'Illumina/MiSeqAnalysis'),
                     os.path.join(CRICK_DX,  'Illumina/MiSeqAnalysis')]

### ____________Run directories derived from S_DRIVE____________###
### _______LOGS________###
S_LOGS = os.path.join(S_DRIVE, 'Logs')
### ______MYELOID______###
NGS_MYE = os.path.join(S_DRIVE, 'NGS_Myeloid')
MYE_RUNS = os.path.join(NGS_MYE, 'Illumina_Runs')
MYE_OLD = os.path.join(MYE_RUNS, 'Older_Runs')
### ________CF_________###
# NGS_CF = os.path.join(S_DRIVE, 'NGS_CF')
# CF_RUNS = os.path.join(NGS_CF, 'MiSeqRuns')
# CF_OLD = os.path.join(CF_RUNS, 'Older_Runs')

### __________________________MySQL DBs_________________________###
FM_DB = 'foundation'
MYE_DB = 'cgw'
SAV_DB = 'sav'
# CF_DB = 'cf'

### ________________________CGW Variables_______________________###

### ________API________###
API_URL = 'https://app.pieriandx.com/cgw-api/v2.0.0/case/'
CGW = {'accept': 'application/json',
       'X-Auth-Email': os.environ.get('cgwuser'),
       'X-Auth-Key': os.environ.get('cgwpw'),
       'X-Auth-Institution': os.environ.get('cgwinstitute')}
#molecular_ngs@upstate.edu:
### ________CGW________###
RA_ROOT = os.path.join(S_DRIVE, 'ra2')
AF = os.path.join(RA_ROOT, 'cgw')
PATIENT_REPORTS = os.path.join(AF, 'patient_reports')
CASE_FILES = os.path.join(AF, 'case_files')
CASE_JSONS = os.path.join(AF, 'case_jsons')
COMPLETE_JSON = os.path.join(CASE_JSONS, 'complete')
INCOMPLETE_JSON = os.path.join(CASE_JSONS, 'incomplete')
CASE_NIRVANA = os.path.join(AF, 'nirvana')

### ________S DRIVE BACKUPS________###
S_DRIVE_BACKUP = os.path.join(RA_ROOT, 'backups')
RHEL = os.path.join(S_DRIVE_BACKUP, 'rhel')
DAILY_BACKUP_DIR = os.path.join(RHEL, 'daily')
WEEKLY_BACKUP_DIR = os.path.join(RHEL, 'weekly')
MONTHLY_BACKUP_DIR = os.path.join(RHEL, 'monthly')
QUARTERLY_BACKUP_DIR = os.path.join(RHEL, 'quarterly')
YEALY_BACKUP_DIR = os.path.join(RHEL, 'yearly')
MANUAL_BACKUP_DIR = os.path.join(RHEL, 'manual')


### _____CHECKLIST_____###
CHECKLIST = os.path.join(AF, 'checklist')
CHECKLIST_XLSX = os.path.join(AF, 'checklist/vc.xlsx')
# RESULTS = os.path.join(NGS_MYE, 'Variant_Checklist/Results')
RESULTS = os.path.join(AF, 'Variant_Checklist/Results')

### _______TEMP________###
TMP = os.path.join(AF, 'tmp')
TEMP_ID = os.path.join(TMP, 'cgw_ids.csv')

### ___POS CONTROL_____###
POS = os.path.join(S_DRIVE, 'NGS_Myeloid/Positive_Control')
POS_BU = os.path.join(AF, 'positive_control')


### ____________________Foundation Variables___________________###
FM_PATH = os.path.join(S_DRIVE, 'FoundationMedicine')
S3_PATH = os.path.join(FM_PATH, 's3data')
REJECT_PATH = os.path.join(S3_PATH, 'rejected')
REJECT_BM = os.path.join(REJECT_PATH, 'biomarkers')
TEMP_PATH = os.path.join(S3_PATH, 'temp')

### _____TRINETX_______###
TNX_HOST = os.environ.get('tnx_address')
TNX_USER = os.environ.get('pathngs_u')
TNX_PASS = os.environ.get('pathngs_p')
TNX_SENT = os.path.join(S3_PATH, 'trinetx_sent/xml_sent.csv')
TNX_DIR = '/Genomics'


### ________HOME where tools/analysis files are stored__________###


# VT = os.path.join(SCRIPTS, 'vt_tool/vt/vt')
NIRVANATOOL = os.path.join(HOME, 'Nirvana')
# NIRVANATOOL = os.path.join(HOME, 'nirvana_tool')
# NIRVANATOOL = os.path.join(AF, 'nirvana_tool') # backup
VCFTOOLS = os.path.join(HOME, 'vcftools')
# HG19 = os.path.join(HOME, 'hg19')
