import pandas as pd
# Load the raw Water Quality Portal PFAS dataset
file_path = "09_Data/PFAS_Clark_County/raw/resultphyschem/resultphyschem.csv"

df = pd.read_csv(file_path)

# Check the size of the dataset
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
# Display all column names
print("\nColumn Names:")
for column in df.columns:
    print(column)
    print("\nFirst 35 Columns:")
for column in df.columns[:35]:
    print(column)
# Select columns relevant to the PFAS analysis
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

pfas = df[columns_to_keep].copy()

print("\nPFAS Analysis Dataset:")
print("Rows:", pfas.shape[0])
print("Columns:", pfas.shape[1])
# Identify PFAS compounds in the dataset
print("\nPFAS Compounds:")
print(pfas["CharacteristicName"].value_counts())
# Check sampling dates
print("\nSampling Dates:")
print(pfas["ActivityStartDate"].value_counts().sort_index())
# Check monitoring locations
print("\nMonitoring Locations:")
print(pfas["MonitoringLocationIdentifier"].value_counts())
print("\nActivity IDs:")
print(pfas["ActivityIdentifier"].value_counts())
# Compare activity types
print("\nActivity Types:")
print(
    pfas[
        ["ActivityIdentifier", "ActivityTypeCode"]
    ].drop_duplicates()
)
# Compare detection conditions by activity type
print("\nDetection Conditions by Activity Type:")
print(
    pfas.groupby(
        ["ActivityTypeCode", "ResultDetectionConditionText"],
        dropna=False
    ).size()
)
# Examine detection/quantitation limits
print("\nDetection Limit Types:")
print(pfas["DetectionQuantitationLimitTypeName"].value_counts(dropna=False))

print("\nDetection Limit Units:")
print(
    pfas["DetectionQuantitationLimitMeasure/MeasureUnitCode"]
    .value_counts(dropna=False)
)
# Examine laboratory reporting level values
print("\nLaboratory Reporting Levels:")
print(
    pfas[
        [
            "CharacteristicName",
            "DetectionQuantitationLimitMeasure/MeasureValue",
            "DetectionQuantitationLimitMeasure/MeasureUnitCode"
        ]
    ]
    .drop_duplicates()
    .sort_values("DetectionQuantitationLimitMeasure/MeasureValue")
    .to_string(index=False)
)
# Separate routine environmental samples from field blanks
routine = pfas[
    pfas["ActivityTypeCode"] == "Sample-Routine"
].copy()

field_blank = pfas[
    pfas["ActivityTypeCode"] == "Quality Control Sample-Field Blank"
].copy()

print("\nRoutine Sample Results:", len(routine))
print("Field Blank Results:", len(field_blank))
print("\nRoutine Sample Reporting Levels:")
print(
    routine[
        [
            "CharacteristicName",
            "DetectionQuantitationLimitMeasure/MeasureValue",
            "DetectionQuantitationLimitMeasure/MeasureUnitCode"
        ]
    ]
    .sort_values("DetectionQuantitationLimitMeasure/MeasureValue")
    .to_string(index=False)
)