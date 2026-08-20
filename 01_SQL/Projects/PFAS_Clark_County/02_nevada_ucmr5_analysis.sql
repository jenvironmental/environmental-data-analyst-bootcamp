-- =====================================================
-- Nevada UCMR 5 PFAS Drinking Water Analysis
-- Environmental Data Analyst Portfolio Project
-- Data Source: EPA UCMR 5
-- =====================================================

-- 1. Verify total PFAS records
SELECT COUNT(*) AS total_records
FROM nevada_ucmr5_pfas;

-- 2. Count unique PFAS compounds
SELECT COUNT(DISTINCT contaminant) AS unique_pfas_compounds
FROM nevada_ucmr5_pfas;

-- 3. Count Nevada public water systems
SELECT COUNT(DISTINCT pwsid) AS public_water_systems
FROM nevada_ucmr5_pfas;

-- 4. Count sampling locations
SELECT COUNT(DISTINCT sample_point_id) AS sampling_locations
FROM nevada_ucmr5_pfas;

-- 5. Review the sampling date range
SELECT
    MIN(collection_date) AS first_sample_date,
    MAX(collection_date) AS last_sample_date
FROM nevada_ucmr5_pfas;
-- 6. Compare results below and at/above the reporting threshold
SELECT
    analytical_results_sign,
    COUNT(*) AS result_count
FROM nevada_ucmr5_pfas
GROUP BY analytical_results_sign
ORDER BY result_count DESC;

-- 7. Count reported PFAS results at or above the MRL by compound
SELECT
    contaminant,
    COUNT(*) AS reported_result_count
FROM nevada_ucmr5_pfas
WHERE analytical_results_sign = '='
GROUP BY contaminant
ORDER BY reported_result_count DESC, contaminant;

-- 8. Count public water systems with reported PFAS results
SELECT
    COUNT(DISTINCT pwsid) AS systems_with_reported_pfas
FROM nevada_ucmr5_pfas
WHERE analytical_results_sign = '=';

-- 9. Count sampling locations with reported PFAS results
SELECT
    COUNT(DISTINCT sample_point_id) AS locations_with_reported_pfas
FROM nevada_ucmr5_pfas
WHERE analytical_results_sign = '=';
-- 10. Summarize reported PFAS concentrations in ng/L
SELECT
    contaminant,
    COUNT(*) AS reported_results,
    ROUND(MIN(result_ng_l)::numeric, 2) AS minimum_ng_l,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP
        (ORDER BY result_ng_l)::numeric, 2) AS median_ng_l,
    ROUND(AVG(result_ng_l)::numeric, 2) AS average_ng_l,
    ROUND(MAX(result_ng_l)::numeric, 2) AS maximum_ng_l
FROM nevada_ucmr5_pfas
WHERE analytical_results_sign = '='
GROUP BY contaminant
ORDER BY reported_results DESC, contaminant;
-- 11. Compare regulated PFAS results with EPA MCL benchmarks
WITH regulated_results AS (
    SELECT
        pwsid,
        pws_name,
        sample_point_id,
        collection_date,
        contaminant,
        result_ng_l,
        CASE
            WHEN contaminant = 'PFOA' THEN 4.0
            WHEN contaminant = 'PFOS' THEN 4.0
            WHEN contaminant = 'PFHxS' THEN 10.0
            WHEN contaminant = 'PFNA' THEN 10.0
            WHEN contaminant = 'HFPO-DA' THEN 10.0
        END AS epa_mcl_ng_l
    FROM nevada_ucmr5_pfas
    WHERE analytical_results_sign = '='
      AND contaminant IN ('PFOA', 'PFOS', 'PFHxS', 'PFNA', 'HFPO-DA')
)

SELECT
    contaminant,
    COUNT(*) AS reported_results,
    COUNT(*) FILTER (
        WHERE result_ng_l > epa_mcl_ng_l
    ) AS above_mcl_benchmark,
    ROUND(MAX(result_ng_l)::numeric, 2) AS maximum_ng_l,
    epa_mcl_ng_l
FROM regulated_results
GROUP BY contaminant, epa_mcl_ng_l
ORDER BY above_mcl_benchmark DESC, contaminant;
-- 12. Identify public water systems with results above EPA MCL benchmarks
WITH regulated_results AS (
    SELECT
        pwsid,
        pws_name,
        sample_point_id,
        contaminant,
        result_ng_l,
        CASE
            WHEN contaminant = 'PFOA' THEN 4.0
            WHEN contaminant = 'PFOS' THEN 4.0
            WHEN contaminant = 'PFHxS' THEN 10.0
            WHEN contaminant = 'PFNA' THEN 10.0
            WHEN contaminant = 'HFPO-DA' THEN 10.0
        END AS epa_mcl_ng_l
    FROM nevada_ucmr5_pfas
    WHERE analytical_results_sign = '='
      AND contaminant IN ('PFOA', 'PFOS', 'PFHxS', 'PFNA', 'HFPO-DA')
)

SELECT
    pwsid,
    pws_name,
    contaminant,
    COUNT(*) AS results_above_benchmark,
    COUNT(DISTINCT sample_point_id) AS sampling_locations,
    ROUND(MAX(result_ng_l)::numeric, 2) AS maximum_ng_l
FROM regulated_results
WHERE result_ng_l > epa_mcl_ng_l
GROUP BY pwsid, pws_name, contaminant
ORDER BY maximum_ng_l DESC;