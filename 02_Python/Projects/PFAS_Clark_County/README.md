# Clark County PFAS Water Quality Analysis

## Project Overview

This project analyzes PFAS water quality data obtained from the Water Quality Portal (WQP). The goal is to practice an environmental data analyst workflow using real environmental monitoring data, from initial data profiling and cleaning in Python to analysis in PostgreSQL.

The dataset contains PFAS laboratory results from one monitoring location, including routine environmental samples and field blank quality-control samples.

## Tools Used

- Python
- pandas
- PostgreSQL
- SQL
- VS Code
- Git and GitHub

## Dataset

The original Water Quality Portal dataset contained:

- 76 laboratory result records
- 81 original fields
- 38 PFAS compounds
- 1 monitoring location
- Sampling date: November 9, 2024
- 38 routine sample results
- 38 field blank QA/QC results

All reported PFAS results were classified as **Not Detected (ND)**.

## Data Profiling

Python and pandas were used to examine:

- Dataset dimensions and column structure
- PFAS compounds analyzed
- Monitoring location and sampling date
- Routine versus quality-control samples
- Detection conditions
- Laboratory reporting limits
- Missing values and data types

## Data Cleaning

The raw dataset was reduced from 81 fields to the variables relevant to the analysis.

Cleaning steps included:

- Renaming Water Quality Portal fields for easier analysis
- Converting the sampling date to a datetime field
- Identifying completely empty fields
- Preserving `ND` results rather than incorrectly converting them to zero
- Creating a separate numeric result field for future quantitative analysis
- Separating routine environmental samples from field blank QA/QC samples
- Exporting cleaned datasets for additional analysis

## SQL Analysis

The cleaned dataset was loaded into PostgreSQL for SQL analysis.

Initial queries examine:

- Total number of records
- Routine versus QA/QC results
- Number of unique PFAS compounds
- Detection status
- Laboratory reporting limits by PFAS compound

## Initial Findings

The dataset contains 38 PFAS compounds analyzed in both a routine environmental sample and a corresponding field blank. No PFAS compounds were reported as detected in either sample type.

Because the laboratory reporting limits vary by compound, a non-detect should not be interpreted as a concentration of zero. The reporting limit provides important context for understanding what the laboratory was capable of detecting for each compound.

## Project Structure

- `01_data_profiling.py` — explores and profiles the raw WQP dataset
- `02_data_cleaning.py` — cleans, restructures, and exports the data
- SQL analysis is maintained in the corresponding `01_SQL/Projects/PFAS_Clark_County` folder
- Raw and processed datasets are maintained in `09_Data/PFAS_Clark_County`

## Next Steps

Future work will expand the SQL analysis and explore opportunities to compare PFAS monitoring results across additional locations, sampling dates, and reporting limits.