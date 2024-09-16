import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Read and filter SPSS data
df = pd.read_spss("Britain/data/BES.sav")[
    [
        "p_edlevelUniW29",
        "churchAttendanceW27",
        "generalElectionVoteW29",
        "wt_new_W29",
        "p_religionW29",
    ]
].dropna()

# Define Christian denominations and filter data
christian_denominations = [
    "Yes - Church of England/Anglican/Episcopal",
    "Yes - Roman Catholic",
    "Yes - Presbyterian/Church of Scotland",
    "Yes - Methodist",
    "Yes - Baptist",
    "Yes - United Reformed Church",
    "Yes - Free Presbyterian",
    "Yes - Brethren",
    "Yes - Orthodox Christian",
    "Yes - Pentecostal",
    "Yes - Evangelical – independent/non-denominational",
]
df = df[df["p_religionW29"].isin(christian_denominations)]

# Define and map education and attendance levels
education_levels = {
    "No qualifications": "No quals",
    "Below GCSE": "Below GCSE",
    "GCSE": "GCSE",
    "A-level": "A-Level",
    "Undergraduate": "Undergraduate",
    "Postgrad": "Postgraduate",
}

attendance_levels = {
    "Never or practically never": "Never",
    "Less often than once a year": "Less than yearly",
    "Less often but at least once a year": "Yearly",
    "Less often but at least twice a year": "Twice yearly",
    "Less often but at least once a month": "Monthly",
    "Less often but at least once in two weeks": "Bi-weekly",
    "Once a week or more": "Weekly+",
}

# Recode education and attendance columns
df["education"] = pd.Categorical(
    df["p_edlevelUniW29"].map(education_levels),
    categories=list(education_levels.values()),
    ordered=True,
)
df["attendance"] = pd.Categorical(
    df["churchAttendanceW27"].map(attendance_levels),
    categories=list(attendance_levels.values()),
    ordered=True,
)
df = df.dropna(subset=["education", "attendance"])

# Define party groups and create vote columns
right_wing_parties = [
    "Conservative",
    "United Kingdom Independence Party (UKIP)",
    "British National Party (BNP)",
    "Brexit Party/Reform UK",
]
left_wing_parties = [
    "Labour",
    "Liberal Democrat",
    "Green Party",
    "Scottish National Party (SNP)",
    "Plaid Cymru",
]

df["vote_right"] = df["generalElectionVoteW29"].isin(right_wing_parties).astype(int)
df["vote_left"] = df["generalElectionVoteW29"].isin(left_wing_parties).astype(int)

# Calculate weighted vote proportions
grouped = (
    df.groupby(["education", "attendance"])
    .agg({"vote_right": "sum", "vote_left": "sum", "wt_new_W29": "sum"})
    .reset_index()
)

grouped["total_votes"] = grouped["vote_right"] + grouped["vote_left"]
grouped["left_percentage"] = (grouped["vote_left"] / grouped["total_votes"]) * 100

# Create heatmap data
heatmap_data = grouped.pivot(
    index="education", columns="attendance", values="left_percentage"
)

# Set up plot style
output_dir = "Britain/output"
os.makedirs(output_dir, exist_ok=True)

fm.fontManager.addfont("Britain/Nunito-VariableFont_wght.ttf")
plt.rcParams["font.family"] = "Nunito"
plt.rcParams["font.weight"] = "bold"

# Create heatmap
plt.figure(figsize=(16, 13))
heatmap = sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".1f",
    cmap=sns.diverging_palette(220, 10, as_cmap=True, center="light"),
    center=50,
    cbar=False,
    vmin=25,
    vmax=75,
    linewidths=0.8,
    annot_kws={"fontsize": 12, "fontweight": "bold"},
)

# Set title and labels
plt.title(
    "Percentage Supporting Left Parties by Education and Church Attendance\nChristians in Great Britain - 2024 GE",
    fontsize=22,
    pad=20,
    fontweight="bold",
)
plt.xlabel("Church Attendance", fontsize=16, labelpad=15, fontweight="bold")
plt.ylabel("Education Level", fontsize=16, labelpad=15, fontweight="bold")
plt.xticks(rotation=45, ha="right", fontsize=12, fontweight="bold")
plt.yticks(fontsize=12, fontweight="bold")

# Add border to plot
for spine in plt.gca().spines.values():
    spine.set_visible(True)
    spine.set_color("#888888")
    spine.set_linewidth(1.5)

plt.tight_layout()
plt.subplots_adjust(bottom=0.25)

# Add colourbar
cbar_ax = plt.gcf().add_axes([0.15, 0.05, 0.7, 0.03])
cbar = plt.colorbar(
    heatmap.collections[0], cax=cbar_ax, orientation="horizontal", aspect=30
)
cbar.set_ticks([25, 37.5, 50, 62.5, 75])
cbar.set_ticklabels(["25%", "37.5%", "50%", "62.5%", "75%"])
cbar.ax.tick_params(labelsize=12)
for label in cbar.ax.get_xticklabels():
    label.set_weight("bold")
cbar.set_label(
    "Percentage Supporting Left Parties", fontsize=14, labelpad=10, fontweight="bold"
)

# Save and display the figure
output_file = os.path.join(output_dir, "church_education_heatmap_left_percentage.png")
plt.savefig(output_file, dpi=300, bbox_inches="tight")
plt.show()
