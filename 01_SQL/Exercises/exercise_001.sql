-- =====================================================
-- Exercise 001
-- Environmental Data Analyst Bootcamp
-- Topic: Basic SQL Queries
-- =====================================================

-- 1. Display all records

SELECT *
FROM water_quality;

-- 2. Display only Clark County samples

SELECT *
FROM water_quality
WHERE county = 'Clark';

-- 3. Display county and contaminant value

SELECT county,
       value
FROM water_quality;

-- 4. Display PFAS samples greater than 6

SELECT site_id,
       value
FROM water_quality
WHERE contaminant = 'PFAS'
  AND value > 6;

-- 5. Sort contaminant values from highest to lowest

SELECT contaminant,
       value
FROM water_quality
ORDER BY value DESC;