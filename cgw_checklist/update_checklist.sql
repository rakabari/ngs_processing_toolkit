UPDATE checked_case, checked
SET
    checked_case.CGW = checked.CGW,
    checked_case.COSMIC = checked.COSMIC,
    checked_case.Known = checked.Known,
    checked_case.Nearby = checked.Nearby,
    checked_case.`Google Scholar` = checked.`Google Scholar`,
    checked_case.Pubmed = checked.Pubmed,
    checked_case.`NCCN FDA` = checked.`NCCN FDA`,
    checked_case.`Clinical Trials` = checked.`Clinical Trials`,
    checked_case.Tier = checked.Tier,
    checked_case.Comments = checked.Comments
WHERE
    checked_case.Variant = checked.Variant;