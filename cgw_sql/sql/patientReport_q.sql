USE cgw;

DROP TABLE
    IF EXISTS Frequency,
    Frequency_in_Disease,
    patient_reportsQ;

CREATE TEMPORARY
TABLE Frequency
SELECT
    CONCAT(
        geneSymbol,
        ":",
        cSyntax,
        ":",
        pSyntax
    ) AS Variant,
    CAST(
        COUNT(
            CONCAT(
                geneSymbol,
                ":",
                cSyntax,
                ":",
                pSyntax
            )
        ) AS CHAR
    ) AS 'Frequency'
FROM patient_reports
GROUP BY
    CONCAT(
        geneSymbol,
        ":",
        cSyntax,
        ":",
        pSyntax
    );

CREATE TABLE
    Frequency_in_Disease
SELECT
    CONCAT(
        geneSymbol,
        ':',
        cSyntax,
        ':',
        pSyntax,
        ':',
        Disease
    ) AS Variant,
    CAST(
        COUNT(
            CONCAT(
                geneSymbol,
                ':',
                cSyntax,
                ':',
                pSyntax,
                ':',
                Disease
            )
        ) AS CHAR
    ) AS 'Frequency_in_Disease'
FROM patient_reports
GROUP BY
    CONCAT(
        geneSymbol,
        ':',
        cSyntax,
        ':',
        pSyntax,
        ':',
        Disease
    );

CREATE TABLE patient_reportsQ
SELECT
    patient_reports.Accession,
    patient_reports.MRN,
    patient_reports.PatientName,
    case_details.SpecimenType,
    patient_reports.DateOfBirth,
    patient_reports.transcript,
    patient_reports.geneSymbol,
    CONCAT(cSyntax, structuralSyntax) AS cSyntax,
    CONCAT(pSyntax, structuralSyntax) AS pSyntax,
    patient_reports.VAF,
    patient_reports.Depth,
    patient_reports.`Level` AS Classification,
    patient_reports.Interpretation,
    patient_reports.SignedoutBy,
    patient_reports.SignedoutDate,
    patient_reports.Disease,
    Frequency.Frequency,
    Frequency_in_Disease.Frequency_in_Disease
FROM patient_reports
    LEFT JOIN Frequency ON CONCAT(
        geneSymbol, ':', cSyntax, ':', pSyntax
    ) = Frequency.Variant
    LEFT JOIN Frequency_in_Disease ON CONCAT(
        geneSymbol, ':', cSyntax, ':', pSyntax, ':', Disease
    ) = Frequency_in_Disease.Variant
    LEFT JOIN case_details ON patient_reports.Accession = case_details.Accession
WHERE
    patient_reports.Accession NOT REGEXP 'CV-PS|M1';

ALTER TABLE patient_reportsQ
ADD
    PK INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

ALTER TABLE
    patient_reportsQ CHANGE COLUMN Interpretation Interpretation VARCHAR(15000) NULL DEFAULT NULL;

DROP TABLE IF EXISTS Frequency, Frequency_in_Disease;