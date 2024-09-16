import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Read the SPSS file
df = pd.read_spss("Britain/data/BES.sav")

# Filter and prepare the data
df = df[["p_gross_householdW29", "generalElectionVoteW29", "wt_new_W29"]]
df = df.dropna()

# Exclude non-voters and "don't know" responses
df = df[~df["generalElectionVoteW29"].isin([0, 99])]

# Create a cross-tabulation of income and voting, weighted by wt_new_W29
crosstab = pd.crosstab(
    df["p_gross_householdW29"],
    df["generalElectionVoteW29"],
    values=df["wt_new_W29"],
    aggfunc="sum",
    normalize="index",
)

# Define income ranges and their midpoints
income_ranges = [
    (0, 5000),
    (5000, 10000),
    (10000, 15000),
    (15000, 20000),
    (20000, 25000),
    (25000, 30000),
    (30000, 35000),
    (35000, 40000),
    (40000, 45000),
    (45000, 50000),
    (50000, 60000),
    (60000, 70000),
    (70000, 100000),
    (100000, 150000),
    (150000, float("inf")),  # Use infinity for the last range
]

midpoints = [
    (start + end) / 2 if end != float("inf") else start * 1.5
    for start, end in income_ranges
]

# Ensure midpoints match the number of rows in crosstab
while len(midpoints) < len(crosstab):
    midpoints.append(midpoints[-1] * 1.1)  # Add extra points if needed

# Define party colors and main parties
party_colors = {
    "Conservative": "#0087DC",  # Blue
    "Labour": "#DC241f",  # Red
    "Liberal Democrat": "#FDBB30",  # Yellow
    "Scottish National Party (SNP)": "#FDF38E",  # Light Yellow
    "Green Party": "#6AB023",  # Green
}

# Set up the plot
plt.figure(figsize=(15, 10))

# Plot lines for each party
for party in party_colors.keys():
    if party in crosstab.columns:
        y = crosstab[party].values
        x = midpoints[: len(y)]  # Use only as many midpoints as there are data points
        plt.plot(x, y, label=party, color=party_colors[party], marker="o")

        # Polynomial regression
        z = np.polyfit(x, y, 3)
        p = np.poly1d(z)
        smooth_x = np.linspace(min(x), max(x), 200)
        plt.plot(smooth_x, p(smooth_x), color=party_colors[party], linestyle="--")

plt.title("Voting Patterns by Annual Household Income")
plt.xlabel("Annual Household Income (£)")
plt.ylabel("Proportion of Votes")
plt.legend(title="Party", loc="center left", bbox_to_anchor=(1, 0.5))
plt.tight_layout()

# Use log scale for x-axis due to large range
plt.xscale("log")

# Format x-axis labels as currency
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"£{x:,.0f}"))

# Update x-axis ticks
plt.xticks(
    midpoints[:len(crosstab)],  # Use only as many midpoints as there are rows in crosstab
    [f"£{int(m):,}" if m != midpoints[-1] else "£150,000+" for m in midpoints[:len(crosstab)]],
    rotation=45,
    ha="right",
)

plt.grid(True, linestyle="--", alpha=0.7)
plt.show()
