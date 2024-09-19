import pandas as pd
import matplotlib.pyplot as plt

# Read the SPSS file
df = pd.read_spss("Britain/data/BES.sav")

# Filter and prepare the data
df = df[["p_ethnicityW29", "wt_new_W29"]]
df = df.dropna()

# Calculate weighted percentages
ethnicity_counts = df.groupby("p_ethnicityW29")["wt_new_W29"].sum()
total_weight = ethnicity_counts.sum()
ethnicity_percentages = (ethnicity_counts / total_weight) * 100

# Sort percentages in descending order
ethnicity_percentages_sorted = ethnicity_percentages.sort_values(ascending=False)

# Update the ethnicity_labels dictionary
ethnicity_labels = df["p_ethnicityW29"].astype("category").cat.categories.tolist()

# Create a bar chart
plt.figure(figsize=(12, 8))
bars = plt.bar(ethnicity_percentages_sorted.index, ethnicity_percentages_sorted.values)

plt.title("Ethnicity Distribution (Weighted)")
plt.xlabel("Ethnicity")
plt.ylabel("Percentage")
plt.xticks(rotation=45, ha="right")

# Add percentage labels on the bars
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2.0,
        height,
        f"{height:.2f}%",
        ha="center",
        va="bottom",
    )

plt.tight_layout()

# Add a legend with ethnicity labels
plt.legend(
    bars,
    ethnicity_labels,
    title="Ethnicity",
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
)

plt.show()

# Print the percentages
print("Ethnicity Percentages:")
for ethnicity, percentage in ethnicity_percentages_sorted.items():
    print(f"{ethnicity_labels[ethnicity]}: {percentage:.2f}%")
