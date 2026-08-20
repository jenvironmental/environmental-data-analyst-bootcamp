import pandas as pd

# Load Nevada statewide PFAS dataset
file_path = (
    "09_Data/PFAS_Clark_County/raw/"
    "nevada_pfas_all_sites_raw/resultphyschem.csv"
)

df = pd.read_csv(file_path, low_memory=False)

print("Nevada PFAS dataset shape:")
print(df.shape)

# Review data providers
print("\nRecords by Provider:")
print(df["ProviderName"].value_counts(dropna=False))

# Review PFAS characteristics/compounds
print("\nCharacteristics:")
print(df["CharacteristicName"].value_counts(dropna=False))

# Review sampling dates
print("\nSampling Dates:")
print(df["ActivityStartDate"].value_counts(dropna=False).sort_index())

# Review detection conditions
print("\nDetection Conditions:")
print(df["ResultDetectionConditionText"].value_counts(dropna=False))