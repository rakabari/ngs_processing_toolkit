USE foundation;

-- Dropping tables if they already exist
DROP TABLE IF EXISTS UNIQUE_CASES_TEMP, TMB_TEMP, MSI_STATUS_TEMP, MSI_LOCI_TEMP, LOH_TEMP, TUMORFRACTION_TEMP, MEDIANCOVERAGE_TEMP, TMB_MSI_LOH, CNV, GR_FUSIONS;

-- ----------------------------Create TEMP Tables----------------------------

-- Creating a distinct list of all cases that will be merged with individual biomarker tables
CREATE TEMPORARY TABLE UNIQUE_CASES_TEMP AS
		SELECT	DISTINCT MRN, FMI_CaseID, PatientName, DOB, Gender, OrderingPhysician, CollectionDate, ReceivedDate, SpecimenSite, DiagnosisSubmitted, SampleID, BlockID, TestType, SpecimenType
		FROM	BIOMARKERS;

-- Creating a temporary table for TMB scores
CREATE TEMPORARY TABLE TMB_TEMP AS
		SELECT	FMI_CaseID, TMB_MSI_status AS TMB_Status, TMB_Score
		FROM	BIOMARKERS
		WHERE	TMB_Score IS NOT NULL;

-- Creating a temporary table for MSI statuses
CREATE TEMPORARY TABLE MSI_STATUS_TEMP AS
		SELECT	FMI_CaseID, TMB_MSI_status AS MSI_Status
		FROM	BIOMARKERS
		WHERE	(TMB_MSI_status IS NOT NULL	AND TMB_Score IS NULL);

-- Creating a temporary table for MSI loci
CREATE TEMPORARY TABLE MSI_LOCI_TEMP AS
		SELECT	FMI_CaseID, MSI AS MSI_Loci
		FROM	BIOMARKERS 
        WHERE	MSI IS NOT NULL;

-- Creating a temporary table for LOH values
CREATE TEMPORARY TABLE LOH_TEMP AS
		SELECT	FMI_CaseID, LOH
		FROM	BIOMARKERS
		WHERE	LOH IS NOT NULL;

-- Creating a temporary table for Tumor Fractions
CREATE TEMPORARY TABLE TUMORFRACTION_TEMP AS
		SELECT	FMI_CaseID, TumorFraction
		FROM	BIOMARKERS
		WHERE	TumorFraction IS NOT NULL;

-- Creating a temporary table for Median Coverage
CREATE TEMPORARY TABLE MEDIANCOVERAGE_TEMP AS
		SELECT	FMI_CaseID, MedianCoverage
		FROM	BIOMARKERS
		WHERE	MedianCoverage IS NOT NULL;

-- -----------Merging all tables into TMB_MSI_LOH using FMI_CaseID------------

CREATE TABLE TMB_MSI_LOH AS
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
	
		CREATE INDEX idx_FMI_CaseID 		ON TMB_MSI_LOH (FMI_CaseID(50));
		CREATE INDEX idx_PatientName 		ON TMB_MSI_LOH (PatientName(100));
		CREATE INDEX idx_SpecimenSite 		ON TMB_MSI_LOH (SpecimenSite(50));
		CREATE INDEX idx_DiagnosisSubmitted ON TMB_MSI_LOH (DiagnosisSubmitted(200));
		CREATE INDEX idx_TestType 			ON TMB_MSI_LOH (TestType(50));
		CREATE INDEX idx_TMB_Status 		ON TMB_MSI_LOH (TMB_Status(30));
		CREATE INDEX idx_MSI_Status 		ON TMB_MSI_LOH (MSI_Status(30));

-- --------------------Creating a table for CNV data---------------------------

CREATE TABLE CNV AS
		SELECT	MRN, FMI_CaseID, PatientName, DOB, Gender, OrderingPhysician, CollectionDate, ReceivedDate, SpecimenSite, DiagnosisSubmitted, SampleID, BlockID, TestType, SpecimenType, CopyNumber, CNV_equivocal, CNV_gene, CNV_exons, CNV_position, CNV_ratio, CNV_status, CNV_type
		FROM 	BIOMARKERS
		WHERE 	CopyNumber IS NOT NULL;

		CREATE INDEX idx_FMI_CaseID 		ON CNV (FMI_CaseID(50));
		CREATE INDEX idx_PatientName 		ON CNV (PatientName(100));
		CREATE INDEX idx_SpecimenSite 		ON CNV (SpecimenSite(50));
		CREATE INDEX idx_DiagnosisSubmitted ON CNV (DiagnosisSubmitted(200));
		CREATE INDEX idx_TestType 			ON CNV (TestType(50));
		CREATE INDEX idx_CNV_gene 			ON CNV (CNV_gene(30));
		CREATE INDEX idx_CNV_status 		ON CNV (CNV_status(30));
		CREATE INDEX idx_CNV_type 			ON CNV (CNV_type(30));

-- --------------------Creating a table for GR data----------------------------

CREATE TABLE GR_FUSIONS AS
		SELECT	MRN, FMI_CaseID, PatientName, DOB, Gender, OrderingPhysician, CollectionDate, ReceivedDate, SpecimenSite, DiagnosisSubmitted, SampleID, BlockID, TestType, SpecimenType, GR_desc, GR_eq, GR_inframe, GR_genes, GR_position, GR_status, GR_reads, GR_type
		FROM 	BIOMARKERS
		WHERE	GR_desc IS NOT NULL;
		
		CREATE INDEX idx_FMI_CaseID 		ON GR_FUSIONS (FMI_CaseID(50));
		CREATE INDEX idx_PatientName 		ON GR_FUSIONS (PatientName(100));
		CREATE INDEX idx_SpecimenSite 		ON GR_FUSIONS (SpecimenSite(50));
		CREATE INDEX idx_DiagnosisSubmitted ON GR_FUSIONS (DiagnosisSubmitted(200));
		CREATE INDEX idx_TestType 			ON GR_FUSIONS (TestType(50));
		CREATE INDEX idx_GR_inframe 		ON GR_FUSIONS (GR_inframe(30));
		CREATE INDEX idx_GR_genes 			ON GR_FUSIONS (GR_genes(50));
		CREATE INDEX idx_GR_status 			ON GR_FUSIONS (GR_status(30));
		CREATE INDEX idx_GR_type 			ON GR_FUSIONS (GR_type(50));

-- Dropping temporary tables (Temp table cleanup)
DROP TABLE IF EXISTS UNIQUE_CASES_TEMP, TMB_TEMP, MSI_STATUS_TEMP, MSI_LOCI_TEMP, LOH_TEMP, TUMORFRACTION_TEMP, MEDIANCOVERAGE_TEMP;
