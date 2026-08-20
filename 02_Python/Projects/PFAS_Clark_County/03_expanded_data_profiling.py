import pandas as pd

# Load expanded Clark County PFAS dataset
file_path = (
   "09_Data/PFAS_Clark_County/raw/"
    "clark_county_pfas_all_sites_82rows.csv"
)

df = pd.read_csv(file_path, low_memory=False)

print("Expanded PFAS dataset shape:")
print(df.shape)
# Review monitoring locations
print("\nMonitoring Locations:")
print(
    df[
        [
            "MonitoringLocationIdentifier",
            "MonitoringLocationName"
        ]
    ]
    .value_counts()
)
# Identify records missing monitoring location information
missing_sites = df[
    df["MonitoringLocationIdentifier"].isna() |
    df["MonitoringLocationName"].isna()
]

print("\nRecords with Missing Site Information:")
print("Count:", len(missing_sites))

print(
    missing_sites[
        [
            "ProviderName",
            "OrganizationIdentifier",
            "MonitoringLocationIdentifier",
            "MonitoringLocationName",
            "ActivityStartDate",
            "CharacteristicName",
            "ResultDetectionConditionText",
            "ResultMeasureValue",
            "ResultMeasure/MeasureUnitCode"
        ]
    ].to_string(index=False)
)