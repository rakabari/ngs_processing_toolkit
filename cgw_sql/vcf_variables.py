#!/home/sbsuser/venv/bin/python3.11

FORMAT_FIELDS = ['VAF_for_report', 'DP_for_report', 'AO_PREF_VariantPlex', 'RO_PREF_VariantPlex', 'UAO_PREF_VariantPlex', 'SFR_PREF_VariantPlex', 'PFP_PREF_VariantPlex', 'PFR_PREF_VariantPlex', 'GL_Freebayes_VariantPlex', 'QA_Freebayes_VariantPlex', 'QR_Freebayes_VariantPlex', 'MQM_PREF_VariantPlex', 'MQMR_PREF_VariantPlex', 'SB_PREF_VariantPlex',
                 'PAF', 'PAR', 'PRF', 'PRR', 'GT', 'DAO', 'DRE', 'DRO', 'FEDSP', 'FEDSR', 'SFP', 'SFR', 'SRE', 'SAO', 'SRO', 'UAF', 'UDP', 'URO']

CNV_SV = ['SVTYPE', 'END', 'EVENT', 'CN', 'Gene_VariantPlex', 'SD_CNV_VariantPlex', 'Pval_CNV_VariantPlex', 'Transcript_VariantPlex', 'GSP2_Count_VariantPlex', 'Threshold_VariantPlex', 'calledBy',
          'VARTYPE', 'CIEND_VariantPlex', 'CIPOS_VariantPlex', 'CICN_VariantPlex', 'IMPRECISE_VariantPlex', 'SVLEN_VariantPlex', 'CNV_MUTTYPE_VariantPlex', 'MAC_VariantPlex', 'ROWID', 'MATEID', 'PUBMEDID_VariantPlex', 'num_unaligned_bases_ITD_VariantPlex',
          'ITD_DUPLICATION_LENGTH_VariantPlex', 'UNIQUE_START_SITES_VariantPlex', 'R2_COUNT_VariantPlex', 'DEPTH_AT_BREAKPOINT_VariantPlex', 'insertion_length_VariantPlex', 'R1_COUNT_VariantPlex', 'GENES_UNIQUE_VariantPlex', 'PERCENT_OF_COVERAGE_VariantPlex', 'EITHER_R1_OR_R2_VariantPlex', 'BOTH_R1_AND_R2_VariantPlex', 'NOVEL_TYPE_VariantPlex', 'Archer_Result_Breakpoints_VariantPlex', 'DNA_Structural_Variant_Processed_Vartype_VariantPlex', 'DNA_Structural_Variant_Is_Complex_VariantPlex']

DROP_COL = ['INFO', 'FORMAT', 'SAMPLE', 'INFO_SPLIT', 'FORMAT_SAMPLE',
            'FILTER', '#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL']

VISION = ['Archer_CosmicID_Vision_VariantPlex', 'Archer_Gene_Vision_VariantPlex',
          'Archer_MutationCDS_Vision_VariantPlex', 'Archer_MutationAA_Vision_VariantPlex', 'CNT_Vision_VariantPlex']

FREEBAYES = ['NS_Freebayes_VariantPlex', 'DPB_Freebayes_VariantPlex', 'AC_Freebayes_VariantPlex', 'AN_Freebayes_VariantPlex', 'RO_Freebayes_VariantPlex', 'AO_Freebayes_VariantPlex', 'PRO_Freebayes_VariantPlex', 'PAO_Freebayes_VariantPlex', 'PQR_Freebayes_VariantPlex', 'PQA_Freebayes_VariantPlex', 'SRP_Freebayes_VariantPlex', 'SAP_Freebayes_VariantPlex', 'AB_Freebayes_VariantPlex', 'ABP_Freebayes_VariantPlex', 'RUN_Freebayes_VariantPlex',
             'RPP_Freebayes_VariantPlex', 'RPPR_Freebayes_VariantPlex', 'RPL_Freebayes_VariantPlex', 'RPR_Freebayes_VariantPlex', 'EPP_Freebayes_VariantPlex', 'EPPR_Freebayes_VariantPlex', 'DPRA_Freebayes_VariantPlex', 'ODDS_Freebayes_VariantPlex', 'GTI_Freebayes_VariantPlex', 'CIGAR_Freebayes_VariantPlex', 'NUMALT_Freebayes_VariantPlex', 'MEANALT_Freebayes_VariantPlex', 'PAIRED_Freebayes_VariantPlex', 'PAIREDR_Freebayes_VariantPlex']

CSQ_COL = ['Allele', 'Consequence', 'IMPACT', 'SYMBOL', 'Gene', 'Feature_type', 'Feature', 'BIOTYPE', 'EXON', 'INTRON', 'HGVSc', 'HGVSp', 'cDNA_position', 'CDS_position', 'Protein_position', 'Amino_acids', 'Codons', 'Existing_variation', 'DISTANCE', 'STRAND', 'FLAGS', 'PICK', 'VARIANT_CLASS', 'SYMBOL_SOURCE', 'HGNC_ID', 'CANONICAL', 'TSL', 'APPRIS', 'CCDS', 'ENSP', 'SWISSPROT', 'TREMBL', 'UNIPARC', 'REFSEQ_MATCH', 'GIVEN_REF', 'USED_REF',
           'BAM_EDIT', 'GENE_PHENO', 'SIFT', 'PolyPhen', 'DOMAINS', 'miRNA', 'HGVS_OFFSET', 'AF', 'AFR_AF', 'AMR_AF', 'EAS_AF', 'EUR_AF', 'SAS_AF', 'AA_AF', 'EA_AF', 'gnomAD_AF', 'gnomAD_AFR_AF', 'gnomAD_AMR_AF', 'gnomAD_ASJ_AF', 'gnomAD_EAS_AF', 'gnomAD_FIN_AF', 'gnomAD_NFE_AF', 'gnomAD_OTH_AF', 'gnomAD_SAS_AF', 'MAX_AF', 'MAX_AF_POPS', 'CLIN_SIG', 'SOMATIC', 'PHENO', 'PUBMED', 'MOTIF_NAME', 'MOTIF_POS', 'HIGH_INF_POS', 'MOTIF_SCORE_CHANGE']

# CSQ_DEL = ['Allele', 'SYMBOL', 'Feature_type', 'Feature',  'BIOTYPE', 'EXON', 'INTRON', 'cDNA_position', 'CDS_position', 'Protein_position', 'Amino_acids', 'Codons', 'Existing_variation', 'DISTANCE', 'FLAGS', 'PICK', 'VARIANT_CLASS', 'SYMBOL_SOURCE', 'HGNC_ID', 'CANONICAL', 'TSL', 'APPRIS', 'CCDS', 'ENSP', 'SWISSPROT', 'TREMBL', 'UNIPARC', 'REFSEQ_MATCH', 'GIVEN_REF', 'USED_REF', 'BAM_EDIT',
#            'GENE_PHENO', 'DOMAINS', 'miRNA', 'HGVS_OFFSET', 'AFR_AF', 'AMR_AF', 'EAS_AF', 'EUR_AF', 'SAS_AF', 'AA_AF', 'EA_AF', 'gnomAD_AFR_AF', 'gnomAD_AMR_AF', 'gnomAD_ASJ_AF', 'gnomAD_EAS_AF', 'gnomAD_FIN_AF', 'gnomAD_NFE_AF', 'gnomAD_OTH_AF', 'gnomAD_SAS_AF', 'AF', 'MAX_AF', 'MAX_AF_POPS', 'SOMATIC', 'PHENO', 'PUBMED', 'MOTIF_NAME', 'MOTIF_POS', 'HIGH_INF_POS', 'MOTIF_SCORE_CHANGE']

GENE_LIST = ['ABL1', 'ANKRD26', 'ASXL1', 'ATRX', 'BCOR', 'BCORL1', 'BRAF', 'BTK', 'CALR', 'CBL', 'CBLB', 'CBLC', 'CCND2', 'CDC25C', 'CDKN2A', 'CEBPA', 'CSF3R', 'CUX1', 'CXCR4', 'DCK', 'DDX41', 'DHX15', 'DNMT3A', 'ETNK1', 'ETV6', 'EZH2', 'FBXW7', 'FLT3', 'GATA1', 'GATA2', 'GNAS', 'HRAS', 'IDH1', 'IDH2', 'IKZF1', 'JAK2', 'JAK3',
             'KDM6A', 'KIT', 'KMT2A', 'KRAS', 'LUC7L2', 'MAP2K1', 'MPL', 'MYC', 'MYD88', 'NF1', 'NOTCH1', 'NPM1', 'NRAS', 'PDGFRA', 'PHF6', 'PPM1D', 'PTEN', 'PTPN11', 'RAD21', 'RBBP6', 'RPS14', 'RUNX1', 'SETBP1', 'SF3B1', 'SH2B3', 'SLC29A1', 'SMC1A', 'SMC3', 'SRSF2', 'STAG2', 'STAT3', 'TET2', 'TP53', 'U2AF1', 'U2AF2', 'WT1', 'XPO1', 'ZRSR2']

BULK_COMB = ['CLNSIG', 'CLNDBN', 'RS', 'COSMIC_ID',
             'MUT_STATUS_CALLS', 'FATHMM_CALLS', 'CONSVAR_LoFreq']

CNV_EXCLUDE = ['END'] + CNV_SV[11:]

NCNV_EXCLUDE = BULK_COMB + VISION + FREEBAYES + \
    [c for c in CSQ_COL if not c.endswith('AF')]

AA = {'Cys': 'C', 'Asp': 'D', 'Ser': 'S', 'Gln': 'Q', 'Lys': 'K', 'Ile': 'I', 'Pro': 'P',
      'Thr': 'T', 'Phe': 'F', 'Asn': 'N', 'Gly': 'G', 'His': 'H', 'Leu': 'L', 'Arg': 'R',
      'Trp': 'W', 'Ala': 'A', 'Val': 'V', 'Glu': 'E', 'Tyr': 'Y', 'Met': 'M', 'Ter': '*'}

VC = {'insertion': 'INDEL', 'deletion': 'INDEL',
      'indel': 'INDEL', 'substitution': 'INDEL'}
