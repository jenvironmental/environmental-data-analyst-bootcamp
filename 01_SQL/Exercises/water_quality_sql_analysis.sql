-- Water Quality Analysis
-- Environmental Data Analyst Portfolio Project

-- 1. Preview the water quality dataset
SELECT *
FROM water_quality
LIMIT 10;

-- 2. Identify the contaminants in the dataset
SELECT DISTINCT contaminant
FROM water_quality
ORDER BY contaminant;

-- 3. Calculate the average measured value for each contaminant
SELECT contaminant, AVG(value) AS average_value
FROM water_quality
GROUP BY contaminant
ORDER BY average_value DESC;

-- 4. Compare average contaminant values by county
SELECT county, contaminant, ROUND(AVG(value), 2) AS average_value
FROM water_quality
GROUP BY county, contaminant
ORDER BY county, average_value DESC;

-- 5. Count the number of samples by county and contaminant
SELECT contaminant, COUNT(*) AS sample_count
FROM water_quality
GROUP BY contaminant
ORDER BY sample_count DESC;

-- 6. Review the range of measured values by contaminant
SELECT contaminant,
       MIN(value) AS minimum_value,
       MAX(value) AS maximum_value
FROM water_quality
GROUP BY contaminant
ORDER BY maximum_value DESC;

-- 7. Calculate the range of measured values for each contaminant
SELECT contaminant,
       MIN(value) AS minimum_value,
       MAX(value) AS maximum_value,
       MAX(value) - MIN(value) AS value_range
FROM water_quality
GROUP BY contaminant
ORDER BY value_range DESC;

