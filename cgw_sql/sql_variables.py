#!/home/sbsuser/venv/bin/python3.11
import os
from utils.global_vars import CGW_SQL_DIR

remove_qc_dup = os.path.join(CGW_SQL_DIR, 'sql/remove_qc_dup.sql')
patientReport_q = os.path.join(CGW_SQL_DIR, 'sql/patientReport_q.sql')
