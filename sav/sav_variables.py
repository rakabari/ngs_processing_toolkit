#!venv/bin/python3.10
from utils.global_vars import SAV_DB, NGSDATA, MYE_RUNS, MYE_OLD

RFPATH_ROOTS = [NGSDATA, MYE_RUNS, MYE_OLD]

COL_INDEX = (('Index Number', 'id'),
             ('Sample ID', 'sample_id'),
             ('Project', 'project_name'),
             ('Index 1_I7', 'index1'),
             ('Index 2_I5', 'index2'),
             ('Percent Reads Identified', 'fraction_mapped'))

COL_READS = (('Total Reads', 'total_reads'),
             ('Total Reads PF', 'total_pf_reads'),
             ('Percent Reads PF', 'total_fraction_mapped_reads'),
             ('CV Reads', 'mapped_reads_cv'),
             ('Min Reads', 'min_mapped_reads'),
             ('Max Reads', 'max_mapped_reads'))

COL_SUM1 = (('Yield Total G', 'yield_g'),
            ('Projected Yield G', 'projected_yield_g'),
            ('Percent Aligned', 'percent_aligned'),
            ('Percent Error Rate', 'error_rate'),
            ('Intensity Cycle 1', 'first_cycle_intensity'),
            ('Percent Q30', 'percent_gt_q30'))

COL_SUM2 = (('Lane', 'lane'),
            ('Tiles', 'tile_count'),
            ('Density', 'density'),
            ('Percent PF', 'percent_pf'),
            ('Legacy Phasing Rate', 'phasing'),
            ('Legacy Prephasing Rate', 'prephasing'),
            ('Phasing Slope', 'phasing_slope'),
            ('Phasing Offset', 'phasing_offset'),
            ('Prephasing Slope', 'prephasing_slope'),
            ('Prephasing Offset', 'prephasing_offset'),
            ('Cluster Count Raw', 'cluster_count'),
            ('Cluster Count PF', 'cluster_count_pf'))

DEL_COL = ['Percent_Error_Rate_R2',
           'Percent_Error_Rate_R3',
           'Legacy_Phasing_Rate_R2',
           'Legacy_Phasing_Rate_R3',
           'Legacy_Phasing_Rate_Non-Indexed',
           'Legacy_Phasing_Rate_Total',
           'Legacy_Prephasing_Rate_R2',
           'Legacy_Prephasing_Rate_R3',
           'Legacy_Prephasing_Rate_Non-Indexed',
           'Legacy_Prephasing_Rate_Total']
