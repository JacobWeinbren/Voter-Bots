import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the SPSS file
df = pd.read_spss("Britain/data/BES.sav")

# Filter and prepare the data
df = df[["homeOwn2W26W27", "generalElectionVoteW29", "wt_new_W29"]]
df = df.dropna()

# Create a cross-tabulation of home ownership and voting, weighted by wt_new_W29
crosstab = pd.crosstab(
    df["homeOwn2W26W27"],
    df["generalElectionVoteW29"],
    values=df["wt_new_W29"],
    aggfunc="sum",
    normalize="index",
)

# Define party colors
party_colors = {
    "Conservative": "#0087DC",  # Blue
    "Labour": "#DC241f",  # Red
    "Liberal Democrat": "#FDBB30",  # Yellow
    "Scottish National Party (SNP)": "#FDF38E",  # Light Yellow
    "Plaid Cymru": "#008142",  # Green
    "United Kingdom Independence Party (UKIP)": "#70147A",  # Purple
    "Green Party": "#6AB023",  # Green
    "Brexit Party/Reform UK": "#12B6CF",  # Light Blue
}

# Set default color for parties not in the dictionary
default_color = "#808080"  # Gray

# Create a color list for the parties in the data
colors = [party_colors.get(party, default_color) for party in crosstab.columns]

# Create a stacked bar chart with specified colors
ax = crosstab.plot(kind="bar", stacked=True, figsize=(15, 10), color=colors)

plt.title("Voting Patterns by Home Ownership")
plt.xlabel("Home Ownership Status")
plt.ylabel("Proportion of Votes")
plt.legend(title="Party", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha="right")

# Add percentage labels on the bars
for c in ax.containers:
    ax.bar_label(c, fmt="%.2f%%", label_type="center")

# Replace numeric labels with home ownership categories
home_ownership_labels = {
    1: "Own outright",
    2: "Own with mortgage",
    3: "Rent from local authority",
    4: "Rent from private landlord",
    5: "Rent from Housing Association",
    6: "Live rent free",
    9999: "Don't know",
}
ax.set_xticklabels([home_ownership_labels.get(x, x) for x in crosstab.index])

plt.show()
