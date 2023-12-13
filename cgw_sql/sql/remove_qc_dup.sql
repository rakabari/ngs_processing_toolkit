DELETE FROM QC_CGW_Metrics
WHERE
    InfoID NOT IN (
        SELECT
            MAX(InfoID)
        FROM QC_CGW_Metrics
        GROUP BY Accession, CaseID