import pandas as pd

# Path to EPA UCMR 5 occurrence data
file_path = (
    "09_Data/PFAS_Clark_County/raw/"
    "ucmr5-occurrence-data-by-state/UCMR5_All_MA_WY.txt"
)

# Read only the first 5 rows to inspect the structure
preview = pd.read_csv(
    file_path,
    sep="\t",
    encoding="latin1",
    nrows=5,
    low_memory=False
)

print("Dataset shape preview:")
print(preview.shape)

print("\nColumn Names:")
for column in preview.columns:
    print(column)

print("\nFirst 5 Rows:")
print(preview.head())

import pandas as pd

# Path to EPA UCMR 5 occurrence data
file_path = (
    "09_Data/PFAS_Clark_County/raw/"
    "ucmr5-occurrence-data-by-state/UCMR5_All_MA_WY.txt"
)

# Read the large EPA file in chunks and keep only Nevada records
nevada_chunks = []

for chunk in pd.read_csv(
    file_path,
    sep="\t",
    encoding="latin1",
    chunksize=50000,
    low_memory=False
):
    nv = chunk[chunk["State"] == "NV"].copy()

    if not nv.empty:
        nevada_chunks.append(nv)

nevada = pd.concat(nevada_chunks, ignore_index=True)

print("Nevada UCMR 5 dataset shape:")
print(nevada.shape)

print("\nNevada public water systems:")
print(nevada["PWSID"].nunique())

print("\nContaminants:")
print(nevada["Contaminant"].value_counts())

# Keep PFAS results only (exclude lithium)
nevada_pfas = nevada[
    nevada["Contaminant"].str.lower() != "lithium"
].copy()

print("\nNevada PFAS dataset shape:")
print(nevada_pfas.shape)

print("\nPFAS compounds:")
print(nevada_pfas["Contaminant"].nunique())

print("\nPublic water systems:")
print(nevada_pfas["PWSID"].nunique())

print("\nSampling locations:")
print(nevada_pfas["SamplePointID"].nunique())

print("\nSampling dates:")
print(nevada_pfas["CollectionDate"].nunique())

print("\nDate range:")
print(nevada_pfas["CollectionDate"].min())
print(nevada_pfas["CollectionDate"].max())

print("\nAnalytical result signs:")
print(nevada_pfas["AnalyticalResultsSign"].value_counts(dropna=False))

# Review PFAS results reported at or above the MRL
reported_results = nevada_pfas[
    nevada_pfas["AnalyticalResultsSign"] == "="
].copy()

print("\nResults reported at or above the MRL:")
print(len(reported_results))

print("\nPFAS compounds reported at or above the MRL:")
print(
    reported_results["Contaminant"]
    .value_counts()
)

print("\nPublic water systems with reported PFAS results:")
print(reported_results["PWSID"].nunique())

print("\nSampling locations with reported PFAS results:")
print(reported_results["SamplePointID"].nunique())

# Review concentrations for PFAS reported at or above the MRL
print("\nReported PFAS concentration summary:")
print(
    reported_results.groupby("Contaminant")["AnalyticalResultValue"]
    .agg(["count", "min", "median", "mean", "max"])
    .round(3)
    .sort_values("count", ascending=False)
)

print("\nUnits:")
print(reported_results["Units"].value_counts(dropna=False))

print("\nMRLs by compound:")
print(
    reported_results.groupby("Contaminant")["MRL"]
    .agg(["min", "max"])
)
# Convert PFAS concentrations from µg/L to ng/L
nevada_pfas["result_ng_L"] = (
    nevada_pfas["AnalyticalResultValue"] * 1000
)

nevada_pfas["mrl_ng_L"] = (
    nevada_pfas["MRL"] * 1000
)

# Review reported results in ng/L
reported_results = nevada_pfas[
    nevada_pfas["AnalyticalResultsSign"] == "="
].copy()

print("\nReported PFAS concentrations in ng/L:")
print(
    reported_results.groupby("Contaminant")["result_ng_L"]
    .agg(["count", "min", "median", "mean", "max"])
    .round(2)
    .sort_values("count", ascending=False)
)
# Review PFOA and PFOS results by water system and sampling location
pfoa_pfos = reported_results[
    reported_results["Contaminant"].isin(["PFOA", "PFOS"])
].copy()

print("\nPFOA and PFOS reported results:")
print(
    pfoa_pfos[
        [
            "PWSID",
            "PWSName",
            "FacilityWaterType",
            "SamplePointID",
            "CollectionDate",
            "Contaminant",
            "result_ng_L",
            "mrl_ng_L"
        ]
    ]
    .sort_values(
        ["Contaminant", "result_ng_L"],
        ascending=[True, False]
    )
    .to_string(index=False)
)
# EPA PFAS drinking-water MCLs (ng/L)
epa_mcls = {
    "PFOA": 4.0,
    "PFOS": 4.0,
    "PFHxS": 10.0,
    "PFNA": 10.0,
    "HFPO-DA": 10.0
}

regulated_results = reported_results[
    reported_results["Contaminant"].isin(epa_mcls)
].copy()

regulated_results["epa_mcl_ng_L"] = (
    regulated_results["Contaminant"].map(epa_mcls)
)

regulated_results["above_mcl_benchmark"] = (
    regulated_results["result_ng_L"]
    > regulated_results["epa_mcl_ng_L"]
)

print("\nResults compared with EPA MCL benchmarks:")
print(
    regulated_results.groupby("Contaminant")
    .agg(
        reported_results=("result_ng_L", "count"),
        above_mcl_benchmark=("above_mcl_benchmark", "sum"),
        maximum_ng_L=("result_ng_L", "max"),
        epa_mcl_ng_L=("epa_mcl_ng_L", "first")
    )
)
# Identify systems and locations with results above EPA MCL benchmarks
above_benchmark = regulated_results[
    regulated_results["above_mcl_benchmark"]
].copy()

print("\nSystems with results above EPA MCL benchmarks:")
print(
    above_benchmark.groupby(
        ["PWSID", "PWSName", "Contaminant"]
    )
    .agg(
        results_above_benchmark=("result_ng_L", "count"),
        maximum_ng_L=("result_ng_L", "max"),
        sampling_locations=("SamplePointID", "nunique")
    )
    .reset_index()
    .sort_values(
        ["maximum_ng_L"],
        ascending=False
    )
    .to_string(index=False)
)
# Save cleaned Nevada PFAS dataset for further analysis
output_path = (
    "09_Data/PFAS_Clark_County/processed/"
    "nevada_ucmr5_pfas_clean.csv"
)

nevada_pfas.to_csv(output_path, index=False)

print("\nSaved cleaned Nevada PFAS dataset:")
print(output_path)
print("Rows saved:", len(nevada_pfas))