USE foundation;

--SNV_INDEL
ALTER TABLE SNV_INDEL 
    CHANGE COLUMN MRN                   MRN                 VARCHAR(50)     NULL DEFAULT NULL,
    CHANGE COLUMN FMI_CaseID            FMI_CaseID          VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN PatientName           PatientName         VARCHAR(100)    NULL DEFAULT NULL,
    CHANGE COLUMN DOB                   DOB                 DATE            NULL DEFAULT NULL,
    CHANGE COLUMN Gender                Gender              VARCHAR(15)     NULL DEFAULT NULL,
    CHANGE COLUMN OrderingPhysician     OrderingPhysician   VARCHAR(100)    NULL DEFAULT NULL,
    CHANGE COLUMN CollectionDate        CollectionDate      DATE            NULL DEFAULT NULL,
    CHANGE COLUMN ReceivedDate          ReceivedDate        DATE            NULL DEFAULT NULL,
    CHANGE COLUMN SpecimenSite          SpecimenSite        VARCHAR(60)     NULL DEFAULT NULL,
    CHANGE COLUMN DiagnosisSubmitted    DiagnosisSubmitted  VARCHAR(100)    NULL DEFAULT NULL,
    CHANGE COLUMN SampleID              SampleID            VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN BlockID               BlockID             VARCHAR(100)    NULL DEFAULT NULL,
    CHANGE COLUMN TestType              TestType            VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN SpecimenType          SpecimenType        VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN Gene                  Gene                VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN Transcript            Transcript          VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN HGVSp                 HGVSp               VARCHAR(100)    NULL DEFAULT NULL,
    CHANGE COLUMN HGVSc                 HGVSc               VARCHAR(600)    NULL DEFAULT NULL,
	CHANGE COLUMN VAF 					VAF 				DECIMAL(5,2) 	NULL DEFAULT NULL ,
	CHANGE COLUMN Depth 				Depth 				SMALLINT 		NULL DEFAULT NULL ;
	CHANGE COLUMN FunctionalEffect      FunctionalEffect    VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN Position              Position            VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN Status                Status              VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN Strand                Strand              VARCHAR(5)      NULL DEFAULT NULL,
    CHANGE COLUMN WildType              WildType            VARCHAR(5)      NULL DEFAULT NULL;

	CREATE INDEX idx_FMI_CaseID 		ON SNV_INDEL (FMI_CaseID);
	CREATE INDEX idx_PatientName 		ON SNV_INDEL (PatientName);
	CREATE INDEX idx_CollectionDate 	ON SNV_INDEL (CollectionDate);
	CREATE INDEX idx_SpecimenSite 		ON SNV_INDEL (SpecimenSite);
	CREATE INDEX idx_DiagnosisSubmitted ON SNV_INDEL (DiagnosisSubmitted);
	CREATE INDEX idx_TestType 			ON SNV_INDEL (TestType);
	CREATE INDEX idx_Gene 			    ON SNV_INDEL (Gene);
	CREATE INDEX idx_HGVSp 		        ON SNV_INDEL (HGVSp);
	CREATE INDEX idx_HGVSc 		        ON SNV_INDEL (HGVSc);
    CREATE INDEX idx_VAF 			    ON SNV_INDEL (VAF);
	CREATE INDEX idx_Depth 			    ON SNV_INDEL (Depth);
	CREATE INDEX idx_FunctionalEffect   ON SNV_INDEL (FunctionalEffect);
	CREATE INDEX idx_Status 		    ON SNV_INDEL (Status);

--BIOMARKERS
ALTER TABLE BIOMARKERS 
	CHANGE COLUMN MRN					MRN 				VARCHAR(50) 	NULL DEFAULT NULL,
    CHANGE COLUMN FMI_CaseID			FMI_CaseID			VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN PatientName			PatientName 		VARCHAR(100) 	NULL DEFAULT NULL,
    CHANGE COLUMN DOB					DOB 				DATE 			NULL DEFAULT NULL,
    CHANGE COLUMN Gender				Gender 				VARCHAR(15)		NULL DEFAULT NULL,
    CHANGE COLUMN OrderingPhysician		OrderingPhysician 	VARCHAR(100) 	NULL DEFAULT NULL,
    CHANGE COLUMN CollectionDate		CollectionDate		DATE 			NULL DEFAULT NULL,
    CHANGE COLUMN ReceivedDate 			ReceivedDate 		DATE 			NULL DEFAULT NULL,
    CHANGE COLUMN SpecimenSite 			SpecimenSite 		VARCHAR(60) 	NULL DEFAULT NULL,
    CHANGE COLUMN DiagnosisSubmitted	DiagnosisSubmitted	VARCHAR(100) 	NULL DEFAULT NULL,
    CHANGE COLUMN SampleID				SampleID 			VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN BlockID				BlockID 			VARCHAR(100) 	NULL DEFAULT NULL,
    CHANGE COLUMN TestType				TestType 			VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN SpecimenType 			SpecimenType 		VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN TMB_MSI_Status 		TMB_MSI_Status 		VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN TMB_Score 			TMB_Score 			DECIMAL(5,2) 	NULL DEFAULT NULL,
    CHANGE COLUMN MSI	 				MSI		 			VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN LOH 					LOH 				VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN TumorFraction 		TumorFraction 		VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN MedianCoverage 		MedianCoverage 		MEDIUMINT 		NULL DEFAULT NULL,
	CHANGE COLUMN CopyNumber 			CopyNumber 			SMALLINT 		NULL DEFAULT NULL,
	CHANGE COLUMN CNV_equivocal 		CNV_equivocal		TINYINT 		NULL DEFAULT NULL,
	CHANGE COLUMN CNV_gene 				CNV_gene 			VARCHAR(30) 	NULL DEFAULT NULL,
	CHANGE COLUMN CNV_exons 			CNV_exons 			VARCHAR(30) 	NULL DEFAULT NULL,
	CHANGE COLUMN CNV_position 			CNV_position 		VARCHAR(60) 	NULL DEFAULT NULL,
	CHANGE COLUMN CNV_ratio 			CNV_ratio 			DECIMAL(5,2) 	NULL DEFAULT NULL,
	CHANGE COLUMN CNV_status 			CNV_status 			VARCHAR(30) 	NULL DEFAULT NULL,
	CHANGE COLUMN CNV_type 				CNV_type 			VARCHAR(30) 	NULL DEFAULT NULL,
	CHANGE COLUMN GR_desc 				GR_desc 			VARCHAR(100) 	NULL DEFAULT NULL,
	CHANGE COLUMN GR_eq 				GR_eq 				TINYINT 		NULL DEFAULT NULL,
	CHANGE COLUMN GR_inframe 			GR_inframe 			VARCHAR(15) 	NULL DEFAULT NULL,
	CHANGE COLUMN GR_genes 				GR_genes 			VARCHAR(60) 	NULL DEFAULT NULL,
	CHANGE COLUMN GR_position 			GR_position			VARCHAR(100) 	NULL DEFAULT NULL,
	CHANGE COLUMN GR_status 			GR_status 			VARCHAR(15) 	NULL DEFAULT NULL,
	CHANGE COLUMN GR_reads 				GR_reads 			SMALLINT 		NULL DEFAULT NULL,
	CHANGE COLUMN GR_type 				GR_type 			VARCHAR(30);
    
	CREATE INDEX idx_FMI_CaseID 		ON BIOMARKERS (FMI_CaseID);
	CREATE INDEX idx_PatientName 		ON BIOMARKERS (PatientName);
	CREATE INDEX idx_CollectionDate 	ON BIOMARKERS (CollectionDate);
	CREATE INDEX idx_SpecimenSite 		ON BIOMARKERS (SpecimenSite);
	CREATE INDEX idx_DiagnosisSubmitted ON BIOMARKERS (DiagnosisSubmitted);
	CREATE INDEX idx_TestType 			ON BIOMARKERS (TestType);
	CREATE INDEX idx_TMB_Score 			ON BIOMARKERS (TMB_Score);
	CREATE INDEX idx_TMB_MSI_Status 	ON BIOMARKERS (TMB_MSI_Status);
	CREATE INDEX idx_CopyNumber 		ON BIOMARKERS (CopyNumber);
	CREATE INDEX idx_CNV_gene 			ON BIOMARKERS (CNV_gene);
	CREATE INDEX idx_CNV_ratio 			ON BIOMARKERS (CNV_ratio);	
	CREATE INDEX idx_CNV_status 		ON BIOMARKERS (CNV_status);
	CREATE INDEX idx_CNV_type 			ON BIOMARKERS (CNV_type);
	CREATE INDEX idx_GR_inframe 		ON BIOMARKERS (GR_inframe);
	CREATE INDEX idx_GR_genes 			ON BIOMARKERS (GR_genes);
	CREATE INDEX idx_GR_status 			ON BIOMARKERS (GR_status);
	CREATE INDEX idx_GR_reads 			ON BIOMARKERS (GR_reads);
	CREATE INDEX idx_GR_type 			ON BIOMARKERS (GR_type );

	CREATE INDEX idx_FMI_CaseID 		ON TMB_MSI_LOH (FMI_CaseID);
	CREATE INDEX idx_PatientName 		ON TMB_MSI_LOH (PatientName);
	CREATE INDEX idx_CollectionDate 	ON TMB_MSI_LOH (CollectionDate);
	CREATE INDEX idx_SpecimenSite 		ON TMB_MSI_LOH (SpecimenSite);
	CREATE INDEX idx_DiagnosisSubmitted ON TMB_MSI_LOH (DiagnosisSubmitted);
	CREATE INDEX idx_TestType 			ON TMB_MSI_LOH (TestType);
	CREATE INDEX idx_TMB_Status 		ON TMB_MSI_LOH (TMB_Status);
	CREATE INDEX idx_TMB_Score 			ON TMB_MSI_LOH (TMB_Score);
	CREATE INDEX idx_MSI_Status 		ON TMB_MSI_LOH (MSI_Status);

	CREATE INDEX idx_FMI_CaseID 		ON CNV (FMI_CaseID);
	CREATE INDEX idx_PatientName 		ON CNV (PatientName);
	CREATE INDEX idx_CollectionDate 	ON CNV (CollectionDate);
	CREATE INDEX idx_SpecimenSite 		ON CNV (SpecimenSite);
	CREATE INDEX idx_DiagnosisSubmitted ON CNV (DiagnosisSubmitted);
	CREATE INDEX idx_TestType 			ON CNV (TestType);
	CREATE INDEX idx_CopyNumber 		ON CNV (CopyNumber);
	CREATE INDEX idx_CNV_gene 			ON CNV (CNV_gene);
	CREATE INDEX idx_CNV_ratio 			ON CNV (CNV_ratio);	
	CREATE INDEX idx_CNV_status 		ON CNV (CNV_status);
	CREATE INDEX idx_CNV_type 			ON CNV (CNV_type);

	CREATE INDEX idx_FMI_CaseID 		ON GR_FUSIONS (FMI_CaseID);
	CREATE INDEX idx_PatientName 		ON GR_FUSIONS (PatientName);
	CREATE INDEX idx_CollectionDate 	ON GR_FUSIONS (CollectionDate);
	CREATE INDEX idx_SpecimenSite 		ON GR_FUSIONS (SpecimenSite);
	CREATE INDEX idx_DiagnosisSubmitted ON GR_FUSIONS (DiagnosisSubmitted);
	CREATE INDEX idx_TestType 			ON GR_FUSIONS (TestType);
	CREATE INDEX idx_GR_inframe 		ON GR_FUSIONS (GR_inframe);
	CREATE INDEX idx_GR_genes 			ON GR_FUSIONS (GR_genes);
	CREATE INDEX idx_GR_status 			ON GR_FUSIONS (GR_status);
	CREATE INDEX idx_GR_reads 			ON GR_FUSIONS (GR_reads);
	CREATE INDEX idx_GR_type 			ON GR_FUSIONS (GR_type);

-- VCF_VARIANTS
ALTER TABLE VCF_VARIANTS 
    CHANGE COLUMN FMI_CaseID            FMI_CaseID          VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN Variant               Variant             VARCHAR(5000)   NULL DEFAULT NULL,
    CHANGE COLUMN VAF                   VAF                 DECIMAL(5,2)    NULL DEFAULT NULL,
    CHANGE COLUMN Depth                 Depth               SMALLINT        NULL DEFAULT NULL,
    CHANGE COLUMN Gene                  Gene                VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN Transcript            Transcript          VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN HGVSc                 HGVSc               VARCHAR(5000)   NULL DEFAULT NULL,
    CHANGE COLUMN HGVSp                 HGVSp               VARCHAR(100)    NULL DEFAULT NULL,
    CHANGE COLUMN COSMIC                COSMIC              VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN EFFECT                EFFECT              VARCHAR(30)     NULL DEFAULT NULL;

	CREATE INDEX idx_FMI_CaseID 		ON VCF_VARIANTS (FMI_CaseID);
	CREATE INDEX idx_VAF 				ON VCF_VARIANTS (VAF);
	CREATE INDEX idx_Gene 				ON VCF_VARIANTS (Gene);
	CREATE INDEX idx_HGVSp 				ON VCF_VARIANTS (HGVSp);
	CREATE INDEX idx_COSMIC 			ON VCF_VARIANTS (COSMIC);
	CREATE INDEX idx_EFFECT 			ON VCF_VARIANTS (EFFECT);
