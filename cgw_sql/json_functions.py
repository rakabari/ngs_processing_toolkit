#!/home/sbsuser/venv/bin/python3.11
import json
import pandas as pd
from functools import reduce


def add_field(df: pd.DataFrame, field: str) -> pd.Series:
    """
    Adds a new column to the DataFrame with the given field name, if it doesn't exist.
    Returns a Series object containing the values of the new or existing field.
    """
    if field not in df.columns:
        df[field] = ''
    return df[field]


def json_pretty(json_path: str) -> None:
    """
    Writes the JSON file at the given path in a pretty-printed format.
    """
    with open(json_path, 'r') as inp:
        json_dict = json.load(inp)
    with open(json_path, 'w') as out:
        json.dump(json_dict, out, indent=4)


def parse_json_report(json_path: str) -> pd.DataFrame:
    """
    Parses JSON report and returns a dictionary of Pandas DataFrames.
    """
    with open(json_path, 'r') as f:
        data = json.loads(f.read())
        Accession = json_path.split('/')[-1].split('_')[1]
        df_vl = []
        d = {i['name']: i for i in data['content']}  # convert list to dict
        try:  # For Tier I, II variants
            TierI_II = d['compactClinicalImplications']['content']['knowledgeBaseResults']
            for e in TierI_II:
                var = e['genomicFinding']['variants'][0]
                df_v = pd.json_normalize(var['displayData'])
                add_field(df_v, 'transcript')
                add_field(df_v, 'pSyntax')
                add_field(df_v, 'cSyntax')
                add_field(df_v, 'structuralSyntax')
                ad = var['additionalDetails']
                df_v['VAF'] = float(ad['vaf'])
                df_v['Depth'] = int(ad['depth'].replace(',', ''))
                df_v['Level'] = e['inferredClassification']['level']
                df_v['VariantCallID'] = var['variantCallId']
                df_v['Interpretation'] = (e.get('interpretation', '')
                                          .replace('Interpretation:', '')
                                          .replace('\n', ' ')
                                          .replace('\t', ' ')
                                          .strip())
                df_v['Accession'] = Accession
                df_vl.append(df_v)
        except KeyError:  # when keys are not present
            print(f'{Accession} : Tier I-II Key Error. Empty DF exported')
            df_v = pd.DataFrame({'Accession': Accession}, index=[0])
            df_vl.append(df_v)
        except TypeError:  # when str insread of dict
            print(f'{Accession} : TypeError Wrong dtype')
            df_v = pd.DataFrame({'Accession': Accession}, index=[0])
            df_vl.append(df_v)

        try:  # For Tier III variants
            TierIII = d['compactVUS']['content']['knowledgeBaseResults']
            for e in TierIII:
                var = e['genomicFinding']['variants'][0]
                df_v = pd.json_normalize(var['displayData'])
                add_field(df_v, 'transcript')
                add_field(df_v, 'pSyntax')
                add_field(df_v, 'cSyntax')
                add_field(df_v, 'structuralSyntax')
                ad = var['additionalDetails']
                df_v['VAF'] = float(ad['vaf'])
                df_v['Depth'] = int(ad['depth'].replace(',', ''))
                df_v['Level'] = e['inferredClassification']['level']
                df_v['VariantCallID'] = var['variantCallId']
                df_v['Interpretation'] = e.get('interpretation', '')
                df_v['Accession'] = Accession
                df_vl.append(df_v)
        except KeyError:
            print(f'{Accession} : Tier III Key Error. Empty DF exported')
            df_v = pd.DataFrame({'Accession': Accession}, index=[0])
            df_vl.append(df_v)

        try:  # concatnate dfs or catch err when no variants reported
            df_vs = pd.concat(df_vl, ignore_index=True)
        except ValueError:  # when wrong dtpye
            print(f'{Accession} : ValueError No Variants Reported')
            df_vs = pd.DataFrame({'Accession': Accession}, index=[0])

        try:  # For Signout details
            Signout = d['compactSignout']['content']
            df_s = pd.DataFrame({'SignedoutBy': Signout['name'],
                                 'SignedoutDate': Signout['date'],
                                 'Accession': Accession}, index=[0])
        except KeyError:
            print(f'{Accession} : Signout Key Error. Empty DF created')
            df_s = pd.DataFrame({'Accession': Accession}, index=[0])

        try:  # For Disease details
            Disease = d['compactReportHeader']['content']['disease']
            df_d = pd.DataFrame({'Disease': Disease,
                                 'Accession': Accession}, index=[0])
        except KeyError:
            print(f'{Accession} : Disease Key Error. Empty DF created')
            df_d = pd.DataFrame({'Accession': Accession}, index=[0])

        try:  # For PatientName
            patient_name = d['compactReportHeader']['content']['patient_name']
            df_p = pd.DataFrame({'PatientName': patient_name,
                                 'Accession': Accession}, index=[0])
        except KeyError:
            print(f'{Accession} : patient_name Key Error. Empty DF created')
            df_p = pd.DataFrame({'Accession': Accession}, index=[0])

        try:  # For Date of Birth
            date_of_birth = d['compactReportHeader']['content']['date_of_birth']
            df_o = pd.DataFrame({'DateOfBirth': date_of_birth,
                                 'Accession': Accession}, index=[0])
        except KeyError:
            print(f'{Accession} : date_of_birth Key Error. Empty DF created')
            df_o = pd.DataFrame({'Accession': Accession}, index=[0])

        try:  # MRN
            mrn = d['compactReportHeader']['content']['mrn'][0]
            df_m = pd.DataFrame({'MRN': mrn,
                                 'Accession': Accession}, index=[0])
        except KeyError:
            print(f'{Accession} : mrn Key Error. Empty DF created')
            df_m = pd.DataFrame({'Accession': Accession}, index=[0])

        try:  # FailedExons
            fe = d['compactFailedExons']['content'].split(':')[2]
            df_f = pd.DataFrame({'FailedExons': fe,
                                 'Accession': Accession}, index=[0])
        except KeyError:
            print(f'{Accession} : FailedExons Key Error. Empty DF created')
            df_f = pd.DataFrame({'Accession': Accession}, index=[0])

        try:  # TestInfo
            tec = d['compactTestInformation']['content']
            te = tec['External Annotation Sources']
            te['CGWversion'] = tec['CGW Version']
            te['AnnotationSource'] = tec['Genomic Annotation Source']
            te = sorted(te.items())
            df_t = pd.DataFrame({'TestInfo': str(te),
                                 'Accession': Accession}, index=[0])
        except KeyError:
            print(f'{Accession} : TestInfo Key Error. Empty DF created')
            df_t = pd.DataFrame({'Accession': Accession}, index=[0])

        ## MERGE ALL DFs ##
        df = reduce(lambda left, right: pd.merge(
            left, right, on='Accession'), [df_vs, df_s, df_d, df_p, df_o, df_m, df_f, df_t])
        df.insert(0, 'Accession', df.pop('Accession'))
    return df
