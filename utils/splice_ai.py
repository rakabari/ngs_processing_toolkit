#!/home/sbsuser/venv/bin/python3.11
from global_vars import MISC_FUNC, HG19
import subprocess
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def add_splice_ai(vcfpath):
    SPLICE_AI = os.path.join(MISC_FUNC, 'venv/bin/spliceai')
    output_vcf = vcfpath.replace('.vcf', '_spliceai.vcf')
    ref = os.path.join(HG19, 'hg19.fa')
    cmd = f'{SPLICE_AI} \
                -I {vcfpath} \
                -O {output_vcf} \
                -R {ref} \
                -A grch37'
    subprocess.run(cmd, shell=True, check=True)
