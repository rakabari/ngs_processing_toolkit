-- Switching to the 'foundation' database
USE foundation;

-- Dropping tables if they already exist
DROP TABLE IF EXISTS UNIQUE_CASES_TEMP, TMB_TEMP, MSI_STATUS_TEMP, MSI_LOCI_TEMP, LOH_TEMP, TUMORFRACTION_TEMP, MEDIANCOVERAGE_TEMP, tmb_msi, cnv_gr;

-- Creating a distinct list of all cases that will be merged with individual biomarker tables
CREATE TEMPORARY TABLE UNIQUE_CASES_TEMP AS
		SELECT	DISTINCT MRN, FMI_CaseID, PatientName, DOB, Gender, OrderingPhysician, CollectionDate, ReceivedDate, SpecimenSite, DiagnosisSubmitted, SampleID, BlockID, TestType, SpecimenType
		FROM	biomarkers;

-- Creating a temporary table for TMB scores
CREATE TEMPORARY TABLE TMB_TEMP AS
		SELECT	FMI_CaseID, TMB_MSI_status AS TMB_Status, TMB_Score
		FROM	biomarkers
		WHERE	TMB_Score IS NOT NULL;

-- Creating a temporary table for MSI statuses
CREATE TEMPORARY TABLE MSI_STATUS_TEMP AS
		SELECT	FMI_CaseID, TMB_MSI_status AS MSI_Status
		FROM	biomarkers
		WHERE	(TMB_MSI_status IS NOT NULL	AND TMB_Score IS NULL);

-- Creating a temporary table for MSI loci
CREATE TEMPORARY TABLE MSI_LOCI_TEMP AS
		SELECT	FMI_CaseID, MSI AS MSI_Loci
		FROM	biomarkers 
        WHERE	MSI IS NOT NULL;

-- Creating a temporary table for LOH values
CREATE TEMPORARY TABLE LOH_TEMP AS
		SELECT	FMI_CaseID, LOH
		FROM	biomarkers
		WHERE	LOH IS NOT NULL;

-- Creating a temporary table for Tumor Fractions
CREATE TEMPORARY TABLE TUMORFRACTION_TEMP AS
		SELECT	FMI_CaseID, TumorFraction
		FROM	biomarkers
		WHERE	TumorFraction IS NOT NULL;

-- Creating a temporary table for Median Coverage
CREATE TEMPORARY TABLE MEDIANCOVERAGE_TEMP AS
		SELECT	FMI_CaseID, MedianCoverage
		FROM	biomarkers
		WHERE	MedianCoverage IS NOT NULL;

-- Merging all tables into tmb_msi using FMI_CaseID
CREATE TABLE tmb_msi AS
		SELECT  	UC.*,
					TM.TMB_Status,
					TM.TMB_Score,
					MS.MSI_Status,
					ML.MSI_Loci,
					LO.LOH,
					TF.TumorFraction,
					MC.MedianCoverage
		FROM 		UNIQUE_CASES_TEMP 	UC
		LEFT JOIN	TMB_TEMP			TM	ON UC.FMI_CaseID = TM.FMI_CaseID
		LEFT JOIN	MSI_STATUS_TEMP		MS	ON UC.FMI_CaseID = MS.FMI_CaseID
		LEFT JOIN	MSI_LOCI_TEMP		ML	ON UC.FMI_CaseID = ML.FMI_CaseID
		LEFT JOIN	LOH_TEMP			LO	ON UC.FMI_CaseID = LO.FMI_CaseID
		LEFT JOIN	TUMORFRACTION_TEMP	TF	ON UC.FMI_CaseID = TF.FMI_CaseID
		LEFT JOIN	MEDIANCOVERAGE_TEMP	MC	ON UC.FMI_CaseID = MC.FMI_CaseID;

-- Creating a table for CNV and GR data
CREATE TABLE cnv_gr AS
		SELECT	MRN, FMI_CaseID, PatientName, DOB, Gender, OrderingPhysician, CollectionDate, ReceivedDate, SpecimenSite, DiagnosisSubmitted, SampleID, BlockID, TestType, SpecimenType, CopyNumber, CNV_equivocal, CNV_gene, CNV_exons, CNV_position, CNV_ratio, CNV_status, CNV_type, GR_desc, GR_eq,	GR_inframe, GR_genes, GR_position, GR_status, GR_reads, GR_type
		FROM 	biomarkers
		WHERE 	CopyNumber IS NOT NULL OR GR_desc IS NOT NULL;

ALTER TABLE tmb_msi 
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
    CHANGE COLUMN TMB_Status 			TMB_Status 			VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN TMB_Score 			TMB_Score 			DECIMAL(5,2) 	NULL DEFAULT NULL,
    CHANGE COLUMN MSI_Status 			MSI_Status 			VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN MSI_Loci 				MSI_Loci 			VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN LOH 					LOH 				VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN TumorFraction 		TumorFraction 		VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN MedianCoverage 		MedianCoverage 		MEDIUMINT 		NULL DEFAULT NULL;
	CREATE INDEX idx_FMI_CaseID 		ON tmb_msi (FMI_CaseID);
	CREATE INDEX idx_PatientName 		ON tmb_msi (PatientName);
	CREATE INDEX idx_CollectionDate 	ON tmb_msi (CollectionDate);
	CREATE INDEX idx_SpecimenSite 		ON tmb_msi (SpecimenSite);
	CREATE INDEX idx_DiagnosisSubmitted ON tmb_msi (DiagnosisSubmitted);
	CREATE INDEX idx_TestType 			ON tmb_msi (TestType);
	CREATE INDEX idx_TMB_Score 			ON tmb_msi (TMB_Score);
	CREATE INDEX idx_MSI_Status 		ON tmb_msi (MSI_Status);

ALTER TABLE cnv_gr 
	CHANGE COLUMN MRN 					MRN 				VARCHAR(50) 	NULL DEFAULT NULL,
    CHANGE COLUMN FMI_CaseID 			FMI_CaseID			VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN PatientName 			PatientName			VARCHAR(100) 	NULL DEFAULT NULL,
    CHANGE COLUMN DOB 					DOB 				DATE 			NULL DEFAULT NULL,
    CHANGE COLUMN Gender				Gender 				VARCHAR(15) 	NULL DEFAULT NULL,
    CHANGE COLUMN OrderingPhysician 	OrderingPhysician 	VARCHAR(100) 	NULL DEFAULT NULL,
    CHANGE COLUMN CollectionDate 		CollectionDate 		DATE 			NULL DEFAULT NULL,
    CHANGE COLUMN ReceivedDate 			ReceivedDate 		DATE 			NULL DEFAULT NULL,
    CHANGE COLUMN SpecimenSite 			SpecimenSite		VARCHAR(60) 	NULL DEFAULT NULL,
    CHANGE COLUMN DiagnosisSubmitted	DiagnosisSubmitted 	VARCHAR(100) 	NULL DEFAULT NULL,
    CHANGE COLUMN SampleID 				SampleID			VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN BlockID 				BlockID 			VARCHAR(100) 	NULL DEFAULT NULL,
    CHANGE COLUMN TestType 				TestType 			VARCHAR(30) 	NULL DEFAULT NULL,
    CHANGE COLUMN SpecimenType 			SpecimenType 		VARCHAR(30) 	NULL DEFAULT NULL,
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
	CHANGE COLUMN GR_type 				GR_type 			VARCHAR(30) 	NULL DEFAULT NULL;
	CREATE INDEX idx_FMI_CaseID			ON cnv_gr (FMI_CaseID);
	CREATE INDEX idx_PatientName 		ON cnv_gr (PatientName);
	CREATE INDEX idx_CollectionDate 	ON cnv_gr (CollectionDate);
	CREATE INDEX idx_SpecimenSite 		ON cnv_gr (SpecimenSite);
	CREATE INDEX idx_DiagnosisSubmitted ON cnv_gr (DiagnosisSubmitted);
	CREATE INDEX idx_TestType 			ON cnv_gr (TestType);
	CREATE INDEX idx_CopyNumber 		ON cnv_gr (CopyNumber);
	CREATE INDEX idx_CNV_gene 			ON cnv_gr (CNV_gene);
	CREATE INDEX idx_CNV_ratio 			ON cnv_gr (CNV_ratio);	
	CREATE INDEX idx_CNV_status 		ON cnv_gr (CNV_status);
	CREATE INDEX idx_CNV_type 			ON cnv_gr (CNV_type);
	CREATE INDEX idx_GR_inframe 		ON cnv_gr (GR_inframe);
	CREATE INDEX idx_GR_genes 			ON cnv_gr (GR_genes);
	CREATE INDEX idx_GR_status 			ON cnv_gr (GR_status);
	CREATE INDEX idx_GR_reads 			ON cnv_gr (GR_reads);
	CREATE INDEX idx_GR_type 			ON cnv_gr (GR_type );

-- Dropping temporary tables (Temp table cleanup)
DROP TABLE IF EXISTS UNIQUE_CASES_TEMP, TMB_TEMP, MSI_STATUS_TEMP, MSI_LOCI_TEMP, LOH_TEMP, TUMORFRACTION_TEMP, MEDIANCOVERAGE_TEMP;
