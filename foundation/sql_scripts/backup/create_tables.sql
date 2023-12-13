CREATE TABLE `SNV_INDEL` (
  `MRN` varchar(50) DEFAULT NULL,
  `FMI_CaseID` varchar(30) DEFAULT NULL,
  `PatientName` varchar(100) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `Gender` varchar(15) DEFAULT NULL,
  `OrderingPhysician` varchar(100) DEFAULT NULL,
  `CollectionDate` date DEFAULT NULL,
  `ReceivedDate` date DEFAULT NULL,
  `SpecimenSite` varchar(60) DEFAULT NULL,
  `DiagnosisSubmitted` varchar(100) DEFAULT NULL,
  `SampleID` varchar(30) DEFAULT NULL,
  `BlockID` varchar(100) DEFAULT NULL,
  `TestType` varchar(30) DEFAULT NULL,
  `SpecimenType` varchar(30) DEFAULT NULL,
  `Gene` varchar(30) DEFAULT NULL,
  `Transcript` varchar(30) DEFAULT NULL,
  `HGVSp` varchar(100) DEFAULT NULL,
  `HGVSc` varchar(600) DEFAULT NULL,
  `VAF` decimal(5,2) DEFAULT NULL,
  `Depth` smallint DEFAULT NULL,
  `Equivocal` tinyint(1) DEFAULT NULL,
  `FunctionalEffect` varchar(30) DEFAULT NULL,
  `Position` varchar(30) DEFAULT NULL,
  `Status` varchar(30) DEFAULT NULL,
  `Strand` varchar(5) DEFAULT NULL,
  `WildType` varchar(5) DEFAULT NULL,
  KEY `idx_FMI_CaseID` (`FMI_CaseID`),
  KEY `idx_PatientName` (`PatientName`),
  KEY `idx_CollectionDate` (`CollectionDate`),
  KEY `idx_SpecimenSite` (`SpecimenSite`),
  KEY `idx_DiagnosisSubmitted` (`DiagnosisSubmitted`),
  KEY `idx_TestType` (`TestType`),
  KEY `idx_Gene` (`Gene`),
  KEY `idx_HGVSp` (`HGVSp`),
  KEY `idx_HGVSc` (`HGVSc`),
  KEY `idx_VAF` (`VAF`),
  KEY `idx_Depth` (`Depth`),
  KEY `idx_FunctionalEffect` (`FunctionalEffect`),
  KEY `idx_Status` (`Status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `BIOMARKERS` (
  `MRN` varchar(50) DEFAULT NULL,
  `FMI_CaseID` varchar(30) DEFAULT NULL,
  `PatientName` varchar(100) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `Gender` varchar(15) DEFAULT NULL,
  `OrderingPhysician` varchar(100) DEFAULT NULL,
  `CollectionDate` date DEFAULT NULL,
  `ReceivedDate` date DEFAULT NULL,
  `SpecimenSite` varchar(60) DEFAULT NULL,
  `DiagnosisSubmitted` varchar(100) DEFAULT NULL,
  `SampleID` varchar(30) DEFAULT NULL,
  `BlockID` varchar(100) DEFAULT NULL,
  `TestType` varchar(30) DEFAULT NULL,
  `SpecimenType` varchar(30) DEFAULT NULL,
  `CopyNumber` smallint DEFAULT NULL,
  `CNV_equivocal` tinyint DEFAULT NULL,
  `CNV_gene` varchar(30) DEFAULT NULL,
  `CNV_exons` varchar(30) DEFAULT NULL,
  `CNV_position` varchar(60) DEFAULT NULL,
  `CNV_ratio` decimal(5,2) DEFAULT NULL,
  `CNV_status` varchar(30) DEFAULT NULL,
  `CNV_type` varchar(30) DEFAULT NULL,
  `GR_desc` varchar(100) DEFAULT NULL,
  `GR_eq` tinyint DEFAULT NULL,
  `GR_inframe` varchar(15) DEFAULT NULL,
  `GR_genes` varchar(60) DEFAULT NULL,
  `GR_position` varchar(100) DEFAULT NULL,
  `GR_status` varchar(15) DEFAULT NULL,
  `GR_reads` smallint DEFAULT NULL,
  `GR_type` varchar(30) DEFAULT NULL,
  `TMB_MSI_Status` varchar(30) DEFAULT NULL,
  `TMB_Score` decimal(5,2) DEFAULT NULL,
  `MSI` varchar(30) DEFAULT NULL,
  `LOH` varchar(30) DEFAULT NULL,
  `TumorFraction` varchar(30) DEFAULT NULL,
  `MedianCoverage` mediumint DEFAULT NULL,
  KEY `idx_FMI_CaseID` (`FMI_CaseID`),
  KEY `idx_PatientName` (`PatientName`),
  KEY `idx_CollectionDate` (`CollectionDate`),
  KEY `idx_SpecimenSite` (`SpecimenSite`),
  KEY `idx_DiagnosisSubmitted` (`DiagnosisSubmitted`),
  KEY `idx_TestType` (`TestType`),
  KEY `idx_TMB_Score` (`TMB_Score`),
  KEY `idx_TMB_MSI_Status` (`TMB_MSI_Status`),
  KEY `idx_CopyNumber` (`CopyNumber`),
  KEY `idx_CNV_gene` (`CNV_gene`),
  KEY `idx_CNV_ratio` (`CNV_ratio`),
  KEY `idx_CNV_status` (`CNV_status`),
  KEY `idx_CNV_type` (`CNV_type`),
  KEY `idx_GR_inframe` (`GR_inframe`),
  KEY `idx_GR_genes` (`GR_genes`),
  KEY `idx_GR_status` (`GR_status`),
  KEY `idx_GR_reads` (`GR_reads`),
  KEY `idx_GR_type` (`GR_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `SNV_INDEL` (
  `MRN` varchar(50) DEFAULT NULL,
  `FMI_CaseID` varchar(30) DEFAULT NULL,
  `PatientName` varchar(100) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `Gender` varchar(15) DEFAULT NULL,
  `OrderingPhysician` varchar(100) DEFAULT NULL,
  `CollectionDate` date DEFAULT NULL,
  `ReceivedDate` date DEFAULT NULL,
  `SpecimenSite` varchar(60) DEFAULT NULL,
  `DiagnosisSubmitted` varchar(100) DEFAULT NULL,
  `SampleID` varchar(30) DEFAULT NULL,
  `BlockID` varchar(100) DEFAULT NULL,
  `TestType` varchar(30) DEFAULT NULL,
  `SpecimenType` varchar(30) DEFAULT NULL,
  `Gene` varchar(30) DEFAULT NULL,
  `Transcript` varchar(30) DEFAULT NULL,
  `HGVSp` varchar(100) DEFAULT NULL,
  `HGVSc` varchar(600) DEFAULT NULL,
  `VAF` double DEFAULT NULL,
  `Depth` double DEFAULT NULL,
  `Equivocal` tinyint(1) DEFAULT NULL,
  `FunctionalEffect` varchar(30) DEFAULT NULL,
  `Position` varchar(30) DEFAULT NULL,
  `Status` varchar(30) DEFAULT NULL,
  `Strand` varchar(5) DEFAULT NULL,
  `WildType` varchar(5) DEFAULT NULL,
  KEY `idx_FMI_CaseID` (`FMI_CaseID`),
  KEY `idx_PatientName` (`PatientName`),
  KEY `idx_CollectionDate` (`CollectionDate`),
  KEY `idx_SpecimenSite` (`SpecimenSite`),
  KEY `idx_DiagnosisSubmitted` (`DiagnosisSubmitted`),
  KEY `idx_TestType` (`TestType`),
  KEY `idx_Gene` (`Gene`),
  KEY `idx_HGVSp` (`HGVSp`),
  KEY `idx_HGVSc` (`HGVSc`),
  KEY `idx_VAF` (`VAF`),
  KEY `idx_Depth` (`Depth`),
  KEY `idx_FunctionalEffect` (`FunctionalEffect`),
  KEY `idx_Status` (`Status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `CNV` (
  `MRN` varchar(50) DEFAULT NULL,
  `FMI_CaseID` varchar(30) DEFAULT NULL,
  `PatientName` varchar(100) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `Gender` varchar(15) DEFAULT NULL,
  `OrderingPhysician` varchar(100) DEFAULT NULL,
  `CollectionDate` date DEFAULT NULL,
  `ReceivedDate` date DEFAULT NULL,
  `SpecimenSite` varchar(60) DEFAULT NULL,
  `DiagnosisSubmitted` varchar(100) DEFAULT NULL,
  `SampleID` varchar(30) DEFAULT NULL,
  `BlockID` varchar(100) DEFAULT NULL,
  `TestType` varchar(30) DEFAULT NULL,
  `SpecimenType` varchar(30) DEFAULT NULL,
  `CopyNumber` smallint DEFAULT NULL,
  `CNV_equivocal` tinyint DEFAULT NULL,
  `CNV_gene` varchar(30) DEFAULT NULL,
  `CNV_exons` varchar(30) DEFAULT NULL,
  `CNV_position` varchar(60) DEFAULT NULL,
  `CNV_ratio` decimal(5,2) DEFAULT NULL,
  `CNV_status` varchar(30) DEFAULT NULL,
  `CNV_type` varchar(30) DEFAULT NULL,
  KEY `idx_FMI_CaseID` (`FMI_CaseID`),
  KEY `idx_PatientName` (`PatientName`),
  KEY `idx_CollectionDate` (`CollectionDate`),
  KEY `idx_SpecimenSite` (`SpecimenSite`),
  KEY `idx_DiagnosisSubmitted` (`DiagnosisSubmitted`),
  KEY `idx_TestType` (`TestType`),
  KEY `idx_CopyNumber` (`CopyNumber`),
  KEY `idx_CNV_gene` (`CNV_gene`),
  KEY `idx_CNV_ratio` (`CNV_ratio`),
  KEY `idx_CNV_status` (`CNV_status`),
  KEY `idx_CNV_type` (`CNV_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `GR_FUSIONS` (
  `MRN` varchar(50) DEFAULT NULL,
  `FMI_CaseID` varchar(30) DEFAULT NULL,
  `PatientName` varchar(100) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `Gender` varchar(15) DEFAULT NULL,
  `OrderingPhysician` varchar(100) DEFAULT NULL,
  `CollectionDate` date DEFAULT NULL,
  `ReceivedDate` date DEFAULT NULL,
  `SpecimenSite` varchar(60) DEFAULT NULL,
  `DiagnosisSubmitted` varchar(100) DEFAULT NULL,
  `SampleID` varchar(30) DEFAULT NULL,
  `BlockID` varchar(100) DEFAULT NULL,
  `TestType` varchar(30) DEFAULT NULL,
  `SpecimenType` varchar(30) DEFAULT NULL,
  `GR_desc` varchar(100) DEFAULT NULL,
  `GR_eq` tinyint DEFAULT NULL,
  `GR_inframe` varchar(15) DEFAULT NULL,
  `GR_genes` varchar(60) DEFAULT NULL,
  `GR_position` varchar(100) DEFAULT NULL,
  `GR_status` varchar(15) DEFAULT NULL,
  `GR_reads` smallint DEFAULT NULL,
  `GR_type` varchar(30) DEFAULT NULL,
  KEY `idx_FMI_CaseID` (`FMI_CaseID`),
  KEY `idx_PatientName` (`PatientName`),
  KEY `idx_CollectionDate` (`CollectionDate`),
  KEY `idx_SpecimenSite` (`SpecimenSite`),
  KEY `idx_DiagnosisSubmitted` (`DiagnosisSubmitted`),
  KEY `idx_TestType` (`TestType`),
  KEY `idx_GR_inframe` (`GR_inframe`),
  KEY `idx_GR_genes` (`GR_genes`),
  KEY `idx_GR_status` (`GR_status`),
  KEY `idx_GR_reads` (`GR_reads`),
  KEY `idx_GR_type` (`GR_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `VCF_VARIANTS` (
  `FMI_CaseID` varchar(30) DEFAULT NULL,
  `Variant` varchar(5000) DEFAULT NULL,
  `VAF` decimal(5,2) DEFAULT NULL,
  `Depth` smallint DEFAULT NULL,
  `Gene` varchar(30) DEFAULT NULL,
  `Transcript` varchar(30) DEFAULT NULL,
  `HGVSc` varchar(5000) DEFAULT NULL,
  `HGVSp` varchar(100) DEFAULT NULL,
  `COSMIC` varchar(30) DEFAULT NULL,
  `EFFECT` varchar(30) DEFAULT NULL,
  KEY `idx_FMI_CaseID` (`FMI_CaseID`),
  KEY `idx_VAF` (`VAF`),
  KEY `idx_Gene` (`Gene`),
  KEY `idx_HGVSp` (`HGVSp`),
  KEY `idx_COSMIC` (`COSMIC`),
  KEY `idx_EFFECT` (`EFFECT`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
