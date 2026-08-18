import pandas as pd
import pandas as pd

# Load the raw Water Quality Portal dataset
file_path = "09_Data/PFAS_Clark_County/raw/resultphyschem/resultphyschem.csv"

df = pd.read_csv(file_path)

print("Raw dataset shape:", df.shape)
# Keep only the columns needed for analysis
columns_to_keep = [
    "OrganizationFormalName",
    "ActivityIdentifier",
    "ActivityTypeCode",
    "ActivityMediaName",
    "ActivityStartDate",
    "MonitoringLocationIdentifier",
    "MonitoringLocationName",
    "ActivityLocation/LatitudeMeasure",
    "ActivityLocation/LongitudeMeasure",
    "CharacteristicName",
    "ResultDetectionConditionText",
    "ResultMeasureValue",
    "ResultMeasure/MeasureUnitCode",
    "MeasureQualifierCode",
    "ResultStatusIdentifier",
    "ResultAnalyticalMethod/MethodName",
    "LaboratoryName",
    "DetectionQuantitationLimitTypeName",
    "DetectionQuantitationLimitMeasure/MeasureValue",
    "DetectionQuantitationLimitMeasure/MeasureUnitCode",
    "ProviderName"
]

clean = df[columns_to_keep].copy()

print("Selected dataset shape:", clean.shape)
# Rename columns for easier analysis
clean = clean.rename(columns={
    "OrganizationFormalName": "organization",
    "ActivityIdentifier": "activity_id",
    "ActivityTypeCode": "activity_type",
    "ActivityMediaName": "sample_media",
    "ActivityStartDate": "sample_date",
    "MonitoringLocationIdentifier": "site_id",
    "MonitoringLocationName": "site_name",
    "ActivityLocation/LatitudeMeasure": "latitude",
    "ActivityLocation/LongitudeMeasure": "longitude",
    "CharacteristicName": "pfas_compound",
    "ResultDetectionConditionText": "detection_condition",
    "ResultMeasureValue": "result_value",
    "ResultMeasure/MeasureUnitCode": "result_unit",
    "MeasureQualifierCode": "qualifier",
    "ResultStatusIdentifier": "result_status",
    "ResultAnalyticalMethod/MethodName": "analytical_method",
    "LaboratoryName": "laboratory",
    "DetectionQuantitationLimitTypeName": "reporting_limit_type",
    "DetectionQuantitationLimitMeasure/MeasureValue": "reporting_limit",
    "DetectionQuantitationLimitMeasure/MeasureUnitCode": "reporting_limit_unit",
    "ProviderName": "provider"
})

print("\nClean Column Names:")
print(clean.columns.tolist())
# Check data types
print("\nData Types:")
print(clean.dtypes)

# Check missing values
print("\nMissing Values:")
print(clean.isnull().sum())
# Inspect result values before converting data types
print("\nResult Values:")
print(clean["result_value"].value_counts(dropna=False))

print("\nResult Units:")
print(clean["result_unit"].value_counts(dropna=False))
# Remove columns that contain no data
clean = clean.drop(columns=["qualifier", "laboratory"])

# Convert sample date to datetime
clean["sample_date"] = pd.to_datetime(clean["sample_date"])

# Create a numeric result column
# ND results remain missing rather than being incorrectly converted to zero
clean["result_value_numeric"] = pd.to_numeric(
    clean["result_value"],
    errors="coerce"
)

print("\nCleaned dataset shape:", clean.shape)

print("\nUpdated Data Types:")
print(clean.dtypes)

print("\nNumeric Result Values:")
print(clean["result_value_numeric"].value_counts(dropna=False))
# Separate routine environmental samples from QA/QC field blanks
routine = clean[
    clean["activity_type"] == "Sample-Routine"
].copy()

field_blank = clean[
    clean["activity_type"] == "Quality Control Sample-Field Blank"
].copy()

print("\nRoutine sample shape:", routine.shape)
print("Field blank shape:", field_blank.shape)
# Save processed datasets
routine.to_csv(
    "09_Data/PFAS_Clark_County/processed/pfas_routine_samples.csv",
    index=False
)

field_blank.to_csv(
    "09_Data/PFAS_Clark_County/processed/pfas_field_blanks.csv",
    index=False
)

clean.to_csv(
    "09_Data/PFAS_Clark_County/processed/pfas_all_clean.csv",
    index=False
)

print("\nProcessed datasets saved successfully.")
# Validate saved dataset counts
print("\nValidation:")
print("All clean records:", len(clean))
print("Routine records:", len(routine))
print("Field blank records:", len(field_blank))
print("Unique PFAS compounds:", clean["pfas_compound"].nunique())
print("Routine detections:", (routine["detection_condition"] != "Not Detected").sum())
print("Field blank detections:", (field_blank["detection_condition"] != "Not Detected").sum())