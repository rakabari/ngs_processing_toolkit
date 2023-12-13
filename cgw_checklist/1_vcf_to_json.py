#!/home/sbsuser/venv/bin/python3.11
# import pypaths  # for cronjob
import os
import shutil
import subprocess
from utils.global_vars import CASE_FILES, CASE_NIRVANA, TEMP, NIRVANATOOL, VCFTOOLS


def copy_vcfs(case_files_path, case_nirvana_path, temp_path):
    """
    Copy VCFs from the source directory to the temporary directory.
    It skips the files that have already been annotated by the Nirvana tool.

    Parameters:
    case_files_path (str): The source directory where the VCF files are stored.
    temp_path (str): The temporary directory where the VCF files are copied.
    """

    # Completed accessions by Nirvana tool
    completed = {file.split('_')[0] for file in os.listdir(case_nirvana_path)}

    for path, _, files in os.walk(case_files_path):
        for file in files:
            accession = file.split('$')[1]
            info_id = file.split('$')[2]

            # Skip completed, non-vcf files and validation cases
            if accession in completed or not file.endswith('.vcf') or 'MD2' not in file:
                continue

            src = os.path.join(path, file)
            dst = os.path.join(temp_path, f'{accession}_{info_id}.vcf')
            shutil.copy(src, dst)

            print(f'INFO: Copied {accession}_{info_id}.vcf to {temp_path}')


def keep_latest_vcf(temp_path):
    """
    Retain the most recent VCF (with the maximum infoid) when there are VCFs.

    Parameters:
    temp_path (str): The directory path where the VCF files are stored.
    """
    id_info = {}
    vcfs = [file for file in os.listdir(temp_path) if file.endswith('vcf')]

    for file in vcfs:
        info_id = int(file.split('_')[1].split('.')[0])
        name = file.split('_')[0]

        # Using max directly on the dictionary assignment
        id_info[name] = max(id_info.get(name, 0), info_id)

    for file in vcfs:
        info_id = int(file.split('_')[1].split('.')[0])

        if info_id not in id_info.values():
            vcf_path = os.path.join(temp_path, file)
            os.remove(vcf_path)
            print(f'INFO: VCF Removed: {file}')


def remove_cnv(vcf_path):
    """
    Removes any CNV lines from a VCF file.
    CNV is not annotated, therefore it is removed from the VCF file.

    Parameters:
    vcf_path (str): The path of the VCF file.
    """
    temp_path = vcf_path.replace('.vcf', '_temp.vcf')

    with open(vcf_path, "r", encoding='utf-8') as infile, open(temp_path, "w", encoding='utf-8') as outfile:
        [outfile.write(line) for line in infile if '<CNV>' not in line]

    # Rename by replacing
    os.replace(temp_path, vcf_path)
    print(f'INFO: {os.path.basename(vcf_path)}: CNV removed')


def cnv_sort(temp_path, vcftools):
    """
    Sorts and removes original unsorted VCFs.

    Parameters:
    temp_path (str): The directory path where the VCF files are stored.
    """
    for file in os.listdir(temp_path):
        if not file.endswith('vcf'):
            continue

        vcf_path = os.path.join(temp_path, file)

        # remove cnvs
        remove_cnv(vcf_path)

        # soft vcf using vcftools for nirvana tool
        vcfsort = os.path.join(vcftools, 'src/perl/vcf-sort')
        sorted_vcf_path = vcf_path.replace('.vcf', '_sorted.vcf')
        cmd = f'{vcfsort} {vcf_path} > {sorted_vcf_path}'
        subprocess.run(cmd, shell=True, check=True)

        # remove unsorted vcf & rename sorted vcf with original name
        os.remove(vcf_path)
        os.replace(sorted_vcf_path, vcf_path)
        print(f'INFO: {file}: Sorted')


def run_nirvana_single_file(vcf_path, nirvana_tool):
    """
    Annotate a single VCF file using the Illumina Nirvana tool. 

    Parameters:
    vcf_path (str): The full path of the VCF file to be annotated.
    nirvana_tool (str): The main directory where Nirvana tool is installed.
    """
    output_name = os.path.basename(vcf_path).split('.vcf')[0]
    output_path = os.path.join(os.path.dirname(vcf_path), output_name)

    cmd = f' dotnet {nirvana_tool}/bin/Release/net6.0/Nirvana.dll \
                -c {nirvana_tool}/Data/Cache/GRCh37/Both \
                --sd {nirvana_tool}/Data/SupplementaryAnnotation/GRCh37 \
                -r {nirvana_tool}/Data/References/Homo_sapiens.GRCh37.Nirvana.dat \
                -i {vcf_path} \
                -o {output_path}'
    subprocess.run(cmd, shell=True, check=True)
    print(f'INFO: {os.path.basename(vcf_path)}: Annotated')


def run_nirvana(temp_path, nirvana_tool):
    """
    Use the Illumina Nirvana tool to annotate all VCF files in a directory. 
    This function uses multi-processing to process multiple files concurrently.

    Parameters:
    temp_path (str): The directory path where the VCF files are stored.
    nirvana_tool (str): The main directory where Nirvana tool is installed.
    """
    for file in os.listdir(temp_path):
        vcf_path = os.path.join(temp_path, file)
        run_nirvana_single_file(vcf_path, nirvana_tool)


def move_json(temp_path, case_nirvana):
    """
    Move the JSON files to the output directory.

    Parameters:
    temp_path (str): The directory path where the JSON files are stored.
    """
    for file in os.listdir(temp_path):
        src = os.path.join(temp_path, file)
        dst = os.path.join(case_nirvana, file)

        shutil.move(src, dst)
        print(f'INFO: Moved to {case_nirvana}: {file}')


if __name__ == '__main__':
    try:
        copy_vcfs(CASE_FILES, CASE_NIRVANA, TEMP)
        keep_latest_vcf(TEMP)
        cnv_sort(TEMP, VCFTOOLS)
        run_nirvana(TEMP, NIRVANATOOL)
        move_json(TEMP, CASE_NIRVANA)
    except Exception as e:
        print(f"ERROR: {e}")

    print(f'INFO: Completed: {os.path.basename(__file__)}\n')
