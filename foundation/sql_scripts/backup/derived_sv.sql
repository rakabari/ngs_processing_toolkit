USE foundation;

DROP TABLE IF EXISTS snv_indel;

CREATE TABLE snv_indel SELECT * FROM shortvariants;

ALTER TABLE snv_indel 
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
    CHANGE COLUMN FunctionalEffect      FunctionalEffect    VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN Position              Position            VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN Status                Status              VARCHAR(30)     NULL DEFAULT NULL,
    CHANGE COLUMN Strand                Strand              VARCHAR(5)      NULL DEFAULT NULL,
    CHANGE COLUMN WildType              WildType            VARCHAR(5)      NULL DEFAULT NULL;

	CREATE INDEX idx_FMI_CaseID 		ON snv_indel (FMI_CaseID);
	CREATE INDEX idx_PatientName 		ON snv_indel (PatientName);
	CREATE INDEX idx_CollectionDate 	ON snv_indel (CollectionDate);
	CREATE INDEX idx_SpecimenSite 		ON snv_indel (SpecimenSite);
	CREATE INDEX idx_DiagnosisSubmitted ON snv_indel (DiagnosisSubmitted);
	CREATE INDEX idx_TestType 			ON snv_indel (TestType);
	CREATE INDEX idx_Gene 			    ON snv_indel (Gene);
	CREATE INDEX idx_HGVSp 		        ON snv_indel (HGVSp);
	CREATE INDEX idx_HGVSc 		        ON snv_indel (HGVSc);
    CREATE INDEX idx_VAF 			    ON snv_indel (VAF);
	CREATE INDEX idx_Depth 			    ON snv_indel (Depth);
	CREATE INDEX idx_FunctionalEffect   ON snv_indel (FunctionalEffect);
	CREATE INDEX idx_Status 		    ON snv_indel (Status);