#!/home/sbsuser/venv/bin/python3.11
import csv
import os
import pandas as pd
import shutil
import xml.etree.ElementTree as ET
from utils.global_vars import REJECT_PATH, REJECT_BM, TEMP_PATH


def shortvars_to_df(xml_path):
    """
    Parses FMI XML patient reports and returns patient information as a DataFrame.

    :param xml_path: (str) path to XML file
    :return: (pandas.DataFrame) DataFrame containing patient information
    """

    # List of headers to include in the CSV file
    headers = ['MRN', 'FMI_CaseID', 'PatientName', 'DOB', 'Gender', 'OrderingPhysician', 'CollectionDate',
               'ReceivedDate', 'SpecimenSite', 'DiagnosisSubmitted', 'SampleID', 'BlockID', 'TestType',
               'SpecimenType', 'Gene', 'Transcript', 'HGVSp', 'HGVSc', 'VAF', 'Depth', 'Equivocal',
               'FunctionalEffect', 'Position', 'Status', 'Strand', 'WildType']

    # Prepare paths
    xml_name = os.path.basename(xml_path)
    file_name = os.path.splitext(xml_name)[0]

    os.makedirs(REJECT_PATH, exist_ok=True)  # to move rejected XMLs
    os.makedirs(TEMP_PATH, exist_ok=True)  # for the CSV file
    temp_csv = os.path.join(TEMP_PATH, f'{file_name}.csv')
    xml2csv = open(temp_csv, 'w')
    xml2csv_writer = csv.writer(xml2csv, quoting=csv.QUOTE_ALL)
    xml2csv_writer.writerow(headers)

    wildtype = "F"
    nucl = None

    ### START XML PARSING ###
    try:
        tree = ET.parse(xml_path)
    except ET.ParseError:
        # If there is an error parsing the file, move it to the rejected directory
        print(f'{xml_name} WARNING: Verify xml format:Not Processed')
        shutil.copy(xml_path,
                    os.path.join(REJECT_PATH, f'{file_name}.format_issue.xml'))

    # Get the root element of the XML file
    root = tree.getroot()

    rr_version = None
    fr_version = None
    vr_version = None

    try:
        # Extract the schema location from the root element
        # Location like http://integration.foundationmedicine.com/reporting/ResultsReport.2.1.xsd
        sl = root.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation']
        # splits off schema location url like ['http:', '', 'integration.foundationmedicine.com', 'reporting', 'ResultsReport.2.1.xsd']
        schema_location = sl.split(' ')[1].split('/')
        for item in schema_location:
            if 'ResultsReport' in item:
                # Strips .xsd and ResultsReport. from script to extract Version #
                # There is no guarantee that FMI will not add an extra subversion placement (2.1.1) to the number
                rr_version = item.strip('.xsd').strip('ResultsReport.')
    except Exception as e:
        # If KeyError, (or any other error, log it and continue with version = None)
        print(f'{xml_name} INFO: ResultsReport SchemaLocation not Found. Checking for FinalReport at Root.')
        rr_version = None
        pass

    try:
        if rr_version is None:
            final_report = root.find('FinalReport')
        elif rr_version == '2.1':
            results_payload = root.find(
                '{http://integration.foundationmedicine.com/reporting}ResultsPayload')
            final_report = results_payload.find('FinalReport')
        else:
            # If rr_version is not empty, and not = to 2.1, then that means a new Schema Version is found.
            print(f'{xml_name} WARNING: New FMI ResultsReport XML Schema Version {rr_version} found. {sl} Parser script will continue...')
            results_payload = root.find(
                '{http://integration.foundationmedicine.com/reporting}ResultsPayload')
            final_report = results_payload.find('FinalReport')
    except Exception as e:
        print(f'{xml_name} WARNING: New FMI ResultsReport XML Schema Version {rr_version} found. {sl} Parser script will continue...')
        results_payload = root.find(
            '{http://integration.foundationmedicine.com/reporting}ResultsPayload')
        final_report = results_payload.find('FinalReport')

    # Get FinalReport XSD Version
    try:
        sl = final_report.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation']
        # splits off schema location url like ['http:', '', 'integration.foundationmedicine.com', 'reporting', 'ResultsReport.2.1.xsd']
        schema_location = sl.split(' ')[1].split('/')
        for item in schema_location:
            if 'ClinicalReport' in item:
                # Uses replace instead of strip function as strip did not strip correctly with '.' character present
                fr_version = item.replace('.xsd', '').replace(
                    'ClinicalReportPage1.', '').replace('ClinicalReport.', '')
    except Exception as e:
        # shutil.copy(xml_path,
        #             os.path.join(REJECT_PATH, f'{file_name}.no_final_report.xml'))
        # If KeyError, (or any other error, print warning and continue with version = None)
        fr_version = None
        pass

    if fr_version is not None and (fr_version != '1.1') and (fr_version != '1.0'):
        print(f'{xml_name} WARNING: New FMI FinalReport XML Schema Version {fr_version} found {sl}. Parser script will continue...')

    ### EXTRACT PATIENT INFO ###
    if final_report is None:
        print(f'{xml_name} WARNING: FinalReport not found:Not Processed')
        shutil.copy(xml_path, os.path.join(
            REJECT_PATH, f'{file_name}.no_final_report.xml'))
    else:
        info = ''
        sample = final_report.find('Sample')
        if sample is None:
            print(f'{xml_name} WARNING: SAMPLE not found:Not Processed')
            shutil.copy(xml_path,
                        os.path.join(REJECT_PATH, f'{file_name}.no_sample.xml'))
        else:
            sid = sample.findtext('SampleId', default="")
            bid = sample.findtext('BlockId', default="")
            ttype = sample.findtext('TestType', default="")
            stype = sample.findtext('SpecFormat', default="")

            s_list = [sid, bid, ttype, stype]

            pmi = final_report.find('PMI')
            mrn = pmi.findtext('MRN', default="")
            fid = pmi.findtext('ReportId', default="")
            pname = pmi.findtext('FullName', default="")
            dob = pmi.findtext('DOB', default="")
            gender = pmi.findtext('Gender', default="")
            prov = pmi.findtext('OrderingMD', default="")
            cdate = pmi.findtext('CollDate', default="1001-01-01")
            rdate = pmi.findtext('ReceivedDate', default="1001-01-01")
            site = pmi.findtext('SpecSite', default="")
            diag = pmi.findtext('SubmittedDiagnosis', default="")

            pmi_list = [mrn, fid, pname, dob, gender,
                        prov, cdate, rdate, site, diag]

            ###  EXTRACT VARIANTS ###
            # New FMI ReportResults version 2.1 has variant-report under the ResultsPayload tag
            # Check results_payload for variant-report
            if rr_version == '2.1':
                variant = results_payload.find(
                    '{http://foundationmedicine.com/compbio/variant-report-external}variant-report')
            elif rr_version is not None and (int(rr_version.split('.')[0]) > 2 or int(rr_version.split('.')[1]) > 1):
                variant = results_payload.find(
                    '{http://foundationmedicine.com/compbio/variant-report-external}variant-report')
            else:
                variant = root.find(
                    '{http://foundationmedicine.com/compbio/variant-report-external}variant-report')

            if variant is None:
                print(f'{xml_name} WARNING: Attribute variant-report is not found.')
                shutil.copy(xml_path,
                            os.path.join(REJECT_PATH, f'{file_name}.no_variant.xml'))
            else:
                # check variant-report schema Version
                try:
                    sl = variant.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation']
                    # splits off schema location url like ['http:', '', 'integration.foundationmedicine.com', 'reporting', 'variant-report-external-2.2.xsd']
                    schema_location = sl.split(' ')[1].split('/')
                    for item in schema_location:
                        if 'variant-report-external' in item:
                            # Strips .xsd and variant-report-external- from script to extract Version #
                            version = item.strip('.xsd').strip(
                                'variant-report-external-')
                        elif 'variant-report-compbio' in item:
                            # Strips .xsd and variant_report_compbio_ from script to extract Version #
                            version = item.strip('.xsd').strip(
                                'variant_report_compbio_')
                except Exception as e:
                    # If KeyError, (or any other error, print warning and continue with version = None)
                    print(e.args)
                    print(
                        f'{xml_name} WARNING: variant-report-external version not Found.')
                    version = None
                    pass

                if version is not None and (version != '2.2') and (version != '2.0'):
                    print(
                        f'{xml_name} WARNING: New FMI Variant-Report XML Schema Version {version} found {sl}. Parser script will continue...')

                ## SHORT VARIANTS ##
                short_var = ''
                for shortvars in variant.findall('{http://foundationmedicine.com/compbio/variant-report-external}short-variants'):
                    for shortvar in shortvars.findall('{http://foundationmedicine.com/compbio/variant-report-external}short-variant'):

                        prot = None
                        nucl = None
                        vdb = None
                        vid = None
                        # note dna-evidence or rna-evidence and compare to samples list. There will only be one or the other.
                        evidence = shortvar.find(
                            '{http://foundationmedicine.com/compbio/variant-report-external}dna-evidence')
                        if evidence is None:
                            evidence = shortvar.find(
                                '{http://foundationmedicine.com/compbio/variant-report-external}rna-evidence')
                            if evidence is None:
                                pass
                                # print(f'{xml_name} INFO: No DNA/RNA evidence')
                            else:
                                nucl = shortvar.get('cds-effect')
                                if nucl[1] != '.':
                                    nucl = "r." + nucl
                        else:
                            nucl = shortvar.get('cds-effect')
                            if nucl[1] != '.':
                                nucl = "c." + nucl

                        prot = shortvar.get('protein-effect')
                        if prot[1] != '.':
                            prot = "p." + prot

                        gn = shortvar.get('gene')
                        af = shortvar.get('percent-reads')
                        dp = shortvar.get('depth')
                        eq = shortvar.get('equivocal', None)
                        fe = shortvar.get('functional-effect')
                        po = shortvar.get('position')
                        st = shortvar.get('status')
                        sd = shortvar.get('strand')
                        tr = shortvar.get('transcript')

                        var_list = [gn, tr, prot, nucl, af,
                                    dp, eq, fe, po, st, sd, wildtype]
                        record_list = pmi_list + s_list + var_list
                        xml2csv_writer.writerow(record_list)
                        info += gn

        ### PERTINENT NEGATIVES ###
        pertnegs = final_report.find('PertinentNegatives')
        if pertnegs is not None:
            for pertneg in pertnegs.findall('PertinentNegative'):
                gene = pertneg.findtext('Gene')
                var_list = [gene, None, 'PertNeg', 'PertNeg',
                            None, None, None, None, None, None, None, 'T']
                record_list = pmi_list + s_list + var_list
                xml2csv_writer.writerow(record_list)
                info += gene

        ### ADD TO LOG OF NON-PROCESSED ###
        if info == '':
            shutil.copy(xml_path,
                        os.path.join(REJECT_PATH, f'{file_name}.no_shortvar_pertneg.xml'))
            print(f'{xml_name} WARNING: ShortVar/PertNeg not found:Not Processed')
        else:
            print(f'{xml_name} INFO: Finished')

    xml2csv.close()
    df = pd.read_csv(temp_csv)
    return df


def biomarkers_to_df(xml_path):
    """
    Parses FMI XML patient reports (Biomarkers) and returns patient information as a DataFrame.

    :param xml_path: (str) path to XML file
    :return: (pandas.DataFrame) DataFrame containing patient information
    """

    # List of headers to include in the CSV file
    headers = ['MRN', 'FMI_CaseID', 'PatientName', 'DOB', 'Gender', 'OrderingPhysician', 'CollectionDate', 'ReceivedDate',
               'SpecimenSite', 'DiagnosisSubmitted', 'SampleID', 'BlockID', 'TestType', 'SpecimenType',
               'CopyNumber', 'CNV_equivocal', 'CNV_gene', 'CNV_exons', 'CNV_position', 'CNV_ratio', 'CNV_status', 'CNV_type',
               'GR_desc', 'GR_eq', 'GR_inframe', 'GR_genes', 'GR_position', 'GR_status', 'GR_reads', 'GR_type',
               'TMB_MSI_status', 'TMB_Score', 'MSI', 'LOH', 'TumorFraction', 'MedianCoverage']

    # Prepare paths
    xml_name = os.path.basename(xml_path)
    file_name = os.path.splitext(xml_name)[0]

    os.makedirs(REJECT_BM, exist_ok=True)  # to move rejected XMLs
    os.makedirs(TEMP_PATH, exist_ok=True)  # for the CSV file
    temp_csv = os.path.join(TEMP_PATH, f'{file_name}.csv')
    xml2csv = open(temp_csv, 'w')
    xml2csv_writer = csv.writer(xml2csv, quoting=csv.QUOTE_ALL)
    xml2csv_writer.writerow(headers)

    ### START XML PARSING ###
    try:
        tree = ET.parse(xml_path)
    except ET.ParseError:
        # If there is an error parsing the file, move it to the rejected directory
        print(f'{xml_name} WARNING: Verify xml format:Not Processed')
        shutil.copy(xml_path, os.path.join(
            REJECT_BM, f'{file_name}.format_issue.xml'))

    # Get the root element of the XML file
    root = tree.getroot()

    rr_version = None
    fr_version = None
    vr_version = None

    try:
        # Extract the schema location from the root element
        # Location like http://integration.foundationmedicine.com/reporting/ResultsReport.2.1.xsd
        sl = root.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation']
        # splits off schema location url like ['http:', '', 'integration.foundationmedicine.com', 'reporting', 'ResultsReport.2.1.xsd']
        schema_location = sl.split(' ')[1].split('/')
        for item in schema_location:
            if 'ResultsReport' in item:
                # Strips .xsd and ResultsReport. from script to extract Version #
                # There is no guarantee that FMI will not add an extra subversion placement (2.1.1) to the number
                rr_version = item.strip('.xsd').strip('ResultsReport.')
    except Exception as e:
        # If KeyError, (or any other error, log it and continue with version = None)
        print(f'{xml_name} INFO: ResultsReport SchemaLocation not Found. Checking for FinalReport at Root.')
        rr_version = None
        pass

    try:
        if rr_version is None:
            final_report = root.find('FinalReport')
        elif rr_version == '2.1':
            results_payload = root.find(
                '{http://integration.foundationmedicine.com/reporting}ResultsPayload')
            final_report = results_payload.find('FinalReport')
        else:
            # If rr_version is not empty, and not = to 2.1, then that means a new Schema Version is found.
            print(f'{xml_name} WARNING: New FMI ResultsReport XML Schema Version {rr_version} found. {sl} Parser script will continue...')
            results_payload = root.find(
                '{http://integration.foundationmedicine.com/reporting}ResultsPayload')
            final_report = results_payload.find('FinalReport')
    except Exception as e:
        print(f'{xml_name} WARNING: New FMI ResultsReport XML Schema Version {rr_version} found. {sl} Parser script will continue...')
        results_payload = root.find(
            '{http://integration.foundationmedicine.com/reporting}ResultsPayload')
        final_report = results_payload.find('FinalReport')

    # Get FinalReport XSD Version
    try:
        sl = final_report.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation']
        # splits off schema location url like ['http:', '', 'integration.foundationmedicine.com', 'reporting', 'ResultsReport.2.1.xsd']
        schema_location = sl.split(' ')[1].split('/')
        for item in schema_location:
            if 'ClinicalReport' in item:
                # Uses replace instead of strip function as strip did not strip correctly with '.' character present
                fr_version = item.replace('.xsd', '').replace(
                    'ClinicalReportPage1.', '').replace('ClinicalReport.', '')
    except Exception as e:
        # shutil.copy(xml_path, os.path.join(REJECT_BM, f'{file_name}.no_final_report.xml'))
        # If KeyError, (or any other error, print warning and continue with version = None)
        fr_version = None
        pass

    if fr_version is not None and (fr_version != '1.1') and (fr_version != '1.0'):
        print(f'{xml_name} WARNING: New FMI FinalReport XML Schema Version {fr_version} found {sl}. Parser script will continue...')

    ### EXTRACT PATIENT INFO ###
    if final_report is None:
        print(f'{xml_name} WARNING: FinalReport not found:Not Processed')
        shutil.copy(xml_path, os.path.join(
            REJECT_BM, f'{file_name}.no_final_report.xml'))
    else:
        info = ''
        sample = final_report.find('Sample')
        if sample is None:
            print(f'{xml_name} WARNING: SAMPLE not found:Not Processed')
            shutil.copy(xml_path, os.path.join(
                REJECT_BM, f'{file_name}.no_sample.xml'))
        else:
            sid = sample.findtext('SampleId', default="")
            bid = sample.findtext('BlockId', default="")
            ttype = sample.findtext('TestType', default="")
            stype = sample.findtext('SpecFormat', default="")

            s_list = [sid, bid, ttype, stype]

            pmi = final_report.find('PMI')
            mrn = pmi.findtext('MRN', default="")
            fid = pmi.findtext('ReportId', default="")
            pname = pmi.findtext('FullName', default="")
            dob = pmi.findtext('DOB', default="")
            gender = pmi.findtext('Gender', default="")
            prov = pmi.findtext('OrderingMD', default="")
            cdate = pmi.findtext('CollDate', default="1001-01-01")
            rdate = pmi.findtext('ReceivedDate', default="1001-01-01")
            site = pmi.findtext('SpecSite', default="")
            diag = pmi.findtext('SubmittedDiagnosis', default="")

            pmi_list = [mrn, fid, pname, dob, gender,
                        prov, cdate, rdate, site, diag]

            ###  EXTRACT VARIANTS ###
            # New FMI ReportResults version 2.1 has variant-report under the ResultsPayload tag
            # Check results_payload for variant-report
            if rr_version == '2.1':
                variant = results_payload.find(
                    '{http://foundationmedicine.com/compbio/variant-report-external}variant-report')
            elif rr_version is not None and (int(rr_version.split('.')[0]) > 2 or int(rr_version.split('.')[1]) > 1):
                variant = results_payload.find(
                    '{http://foundationmedicine.com/compbio/variant-report-external}variant-report')
            else:
                variant = root.find(
                    '{http://foundationmedicine.com/compbio/variant-report-external}variant-report')

            if variant is None:
                print(f'{xml_name} WARNING: Attribute variant-report is not found.')
                shutil.copy(xml_path, os.path.join(
                    REJECT_BM, f'{file_name}.no_variant.xml'))
            else:
                # check variant-report schema Version
                try:
                    sl = variant.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation']
                    # splits off schema location url like ['http:', '', 'integration.foundationmedicine.com', 'reporting', 'variant-report-external-2.2.xsd']
                    schema_location = sl.split(' ')[1].split('/')
                    for item in schema_location:
                        if 'variant-report-external' in item:
                            # Strips .xsd and variant-report-external- from script to extract Version #
                            version = item.strip('.xsd').strip(
                                'variant-report-external-')
                        elif 'variant-report-compbio' in item:
                            # Strips .xsd and variant_report_compbio_ from script to extract Version #
                            version = item.strip('.xsd').strip(
                                'variant_report_compbio_')
                except Exception as e:
                    # If KeyError, (or any other error, print warning and continue with version = None)
                    print(e.args)
                    print(
                        f'{xml_name} WARNING: variant-report-external version not Found.')
                    version = None
                    pass

                if version is not None and (version != '2.2') and (version != '2.0'):
                    print(
                        f'{xml_name} WARNING: New FMI Variant-Report XML Schema Version {version} found {sl}. Parser script will continue...')

                ##  Copy Number Alterations ##
                for cnas in variant.findall('{http://foundationmedicine.com/compbio/variant-report-external}copy-number-alterations'):
                    for cna in cnas:
                        cnv_cn = str(cna.get('copy-number', ''))
                        cnv_eq = str(cna.get('equivocal', ''))
                        cnv_gene = str(cna.get('gene', ''))
                        cnv_exons = str(cna.get('number-of-exons', ''))
                        cnv_pos = str(cna.get('position', ''))
                        cnv_ratio = str(cna.get('ratio', ''))
                        cnv_status = str(cna.get('status', ''))
                        cnv_type = str(cna.get('type', ''))

                        var_list = [cnv_cn, cnv_eq, cnv_gene,
                                    cnv_exons, cnv_pos, cnv_ratio, cnv_status, cnv_type,
                                    None, None, None, None, None, None, None, None,
                                    None, None, None]
                        record_list = pmi_list + s_list + var_list
                        xml2csv_writer.writerow(record_list)
                        info += cnv_cn

                ##  Gene Rearrangements ##
                for ras in variant.findall('{http://foundationmedicine.com/compbio/variant-report-external}rearrangements'):
                    for ra in ras:
                        gr_desc = str(ra.get('description', ''))
                        gr_eq = str(ra.get('equivocal', ''))
                        gr_inframe = str(ra.get('in-frame', ''))
                        gr_genes = f"{ra.get('targeted-gene','')}|{ra.get('other-gene','')}"
                        gr_pos = f"{ra.get('pos1','')}|{ra.get('pos2','')}"
                        gr_status = str(ra.get('status', ''))
                        gr_reads = str(ra.get('supporting-read-pairs', ''))
                        gr_type = str(ra.get('type', ''))

                        var_list = [None, None, None, None, None, None, None, None,
                                    gr_desc, gr_eq, gr_inframe, gr_genes, gr_pos,
                                    gr_status, gr_reads, gr_type,
                                    None, None, None]
                        record_list = pmi_list + s_list + var_list
                        xml2csv_writer.writerow(record_list)
                        info += gr_desc

                ## BioMarkers ##
                for bmrks in variant.findall('{http://foundationmedicine.com/compbio/variant-report-external}biomarkers'):
                    for bmrk in bmrks:
                        tmb_msi_st = str(bmrk.get('status', ''))
                        tmb_score = str(bmrk.get('score', ''))

                        var_list = [None, None, None, None, None, None, None, None,
                                    None, None, None, None, None, None, None, None,
                                    tmb_msi_st, tmb_score]
                        record_list = pmi_list + s_list + var_list
                        xml2csv_writer.writerow(record_list)
                        info += tmb_msi_st

        ### Report Properties ###
        repPros = final_report.find('reportProperties')
        if repPros is not None:
            for repPro in repPros.findall('reportProperty'):

                msi = ''
                if 'MicrosatelliteStatusScore' in repPro.get('key'):
                    for prop in repPro:
                        msi += prop.text

                loh = ''
                if 'LossOfHeterozygosityScore' in repPro.get('key'):
                    for prop in repPro:
                        loh += prop.text

                tumor_fr = ''
                if 'TumorFractionScore' in repPro.get('key'):
                    for prop in repPro:
                        tumor_fr += prop.text

                medcov = ''
                if 'MedianCoverageValue' in repPro.get('key'):
                    for prop in repPro:
                        medcov += prop.text.replace('x', '').replace(',', '')

                var_list = [None, None, None, None, None, None, None, None,
                            None, None, None, None, None, None, None, None,
                            None, None,
                            msi, loh, tumor_fr, medcov]
                record_list = pmi_list + s_list + var_list
                xml2csv_writer.writerow(record_list)
                info += f'{msi}{loh}{tumor_fr}{medcov}'

        ### ADD TO LOG OF NON-PROCESSED ###
        if info == '':
            shutil.copy(xml_path, os.path.join(
                REJECT_BM, f'{file_name}.no_biomarkers.xml'))
            print(f'{xml_name} WARNING: BioMarkers not found')
        else:
            print(f'{xml_name} INFO: BioMarkers Finished')

    xml2csv.close()
    df = pd.read_csv(temp_csv)
    return df
