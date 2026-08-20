import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned Nevada UCMR 5 PFAS dataset
file_path = (
    "09_Data/PFAS_Clark_County/processed/"
    "nevada_ucmr5_pfas_clean.csv"
)

df = pd.read_csv(file_path)

# Keep results reported at or above the MRL
reported = df[df["AnalyticalResultsSign"] == "="].copy()

# Count reported results by PFAS compound
occurrence = (
    reported["Contaminant"]
    .value_counts()
    .sort_values()
)
# Create horizontal bar chart
fig, ax = plt.subplots(figsize=(10, 6))

occurrence.plot(
    kind="barh",
    ax=ax
)

# Add result counts to the end of each bar
for container in ax.containers:
    ax.bar_label(container, padding=4)

ax.set_title(
    "PFAS Occurrence in Nevada Drinking Water\n"
    "EPA UCMR 5 Monitoring"
)

ax.set_xlabel("Number of Results at or Above the MRL")
ax.set_ylabel("PFAS Compound")

# Add a little extra space for bar labels
ax.set_xlim(0, occurrence.max() + 3)

# Source / interpretation note
fig.text(
    0.5,
    0.01,
    "Reported results represent measurements at or above the EPA UCMR 5 minimum reporting level (MRL).",
    ha="center",
    fontsize=9
)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(
    "05_Projects/PFAS_Clark_County/figures/"
    "01_pfas_occurrence_nevada.png",
    dpi=300,
    bbox_inches="tight"
    )
plt.show()

# =====================================================
# Chart 2: Maximum reported PFAS concentrations
# =====================================================

max_concentration = (
    reported.groupby("Contaminant")["result_ng_L"]
    .max()
    .sort_values()
)

fig, ax = plt.subplots(figsize=(10, 6))

max_concentration.plot(
    kind="barh",
    ax=ax
)

# Add concentration labels
for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.1f",
        padding=4
    )

ax.set_title(
    "Maximum Reported PFAS Concentrations in Nevada Drinking Water\n"
    "EPA UCMR 5 Monitoring"
)

ax.set_xlabel("Maximum Concentration (ng/L)")
ax.set_ylabel("PFAS Compound")

ax.set_xlim(0, max_concentration.max() + 5)

fig.text(
    0.5,
    0.01,
    "Includes PFAS measurements reported at or above the EPA UCMR 5 minimum reporting level (MRL).",
    ha="center",
    fontsize=9
)

plt.tight_layout(rect=[0, 0.05, 1, 1])

plt.savefig(
    "05_Projects/PFAS_Clark_County/figures/"
    "02_pfas_max_concentration_nevada.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# =====================================================
# Chart 3: PFOA and PFOS above current EPA MCL benchmarks
# =====================================================

mcls = {
    "PFOA": 4.0,
    "PFOS": 4.0
}

regulated = reported[
    reported["Contaminant"].isin(mcls)
].copy()

regulated["epa_mcl_ng_L"] = regulated["Contaminant"].map(mcls)

above_mcl = regulated[
    regulated["result_ng_L"] > regulated["epa_mcl_ng_L"]
].copy()

system_summary = (
    above_mcl.groupby(["PWSName", "Contaminant"])["result_ng_L"]
    .max()
    .unstack(fill_value=0)
)

# Order systems by highest reported concentration
system_summary["max_result"] = system_summary.max(axis=1)
system_summary = system_summary.sort_values(
    "max_result",
    ascending=True
)
system_summary = system_summary.drop(columns="max_result")

fig, ax = plt.subplots(figsize=(11, 6))

system_summary.plot(
    kind="barh",
    ax=ax
)

# Add concentration values to bars
for container in ax.containers:
    labels = [
        f"{bar.get_width():.1f}" if bar.get_width() > 0 else ""
        for bar in container
    ]
    ax.bar_label(container, labels=labels, padding=4)

ax.set_title(
    "Maximum PFOA and PFOS Results Above Current EPA MCLs\n"
    "Nevada UCMR 5 Drinking Water Monitoring"
)

ax.set_xlabel("Maximum Concentration (ng/L)")
ax.set_ylabel("Public Water System")

ax.set_xlim(0, system_summary.max().max() + 5)

fig.text(
    0.5,
    0.01,
    "Current EPA MCLs: PFOA = 4 ng/L and PFOS = 4 ng/L. "
    "Individual UCMR results above an MCL do not by themselves establish a compliance violation.",
    ha="center",
    fontsize=9
)

plt.tight_layout(rect=[0, 0.06, 1, 1])

plt.savefig(
    "05_Projects/PFAS_Clark_County/figures/"
    "03_pfoa_pfos_system_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()