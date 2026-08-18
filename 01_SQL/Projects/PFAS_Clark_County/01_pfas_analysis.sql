-- =====================================================
-- Clark County PFAS Water Quality Analysis
-- Environmental Data Analyst Portfolio Project
-- Data Source: Water Quality Portal
-- =====================================================

-- 1. Preview the cleaned PFAS dataset
SELECT *
FROM pfas_results
LIMIT 10;

-- 2. Verify the number of imported records
SELECT COUNT(*) AS total_records
FROM pfas_results;

-- 3. Compare routine samples and quality control samples
SELECT
    activity_type,
    COUNT(*) AS result_count
FROM pfas_results
GROUP BY activity_type
ORDER BY result_count DESC;
-- 4. Count the number of PFAS compounds analyzed
SELECT
    COUNT(DISTINCT pfas_compound) AS unique_pfas_compounds
FROM pfas_results;
-- 5. Review PFAS detection status for routine environmental samples
SELECT
    detection_condition,
    COUNT(*) AS result_count
FROM pfas_results
WHERE activity_type = 'Sample-Routine'
GROUP BY detection_condition
ORDER BY result_count DESC;
-- 6. Summarize laboratory reporting limits for routine samples
SELECT
    MIN(reporting_limit) AS minimum_reporting_limit,
    MAX(reporting_limit) AS maximum_reporting_limit,
    ROUND(AVG(reporting_limit)::numeric, 2) AS average_reporting_limit
FROM pfas_results
WHERE activity_type = 'Sample-Routine';
-- 7. Identify PFAS compounds with the highest reporting limits
SELECT
    pfas_compound,
    reporting_limit,
    reporting_limit_unit
FROM pfas_results
WHERE activity_type = 'Sample-Routine'
ORDER BY reporting_limit DESC, pfas_compound;
-- 8. Count PFAS compounds by laboratory reporting limit
SELECT
    reporting_limit,
    reporting_limit_unit,
    COUNT(*) AS compound_count
FROM pfas_results
WHERE activity_type = 'Sample-Routine'
GROUP BY reporting_limit, reporting_limit_unit
ORDER BY reporting_limit;

