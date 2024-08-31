import pyreadstat
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Read the .dta file
file_path = os.path.join(script_dir, "data", "2021.dta")
df, meta = pyreadstat.read_dta(file_path)

if "cps21_province" in df.columns:
    print("\nResponses to cps21_province:")
    value_counts = df["cps21_imp_iss"].value_counts()
    print(value_counts)

    # Create the output file path for value counts
    output_file = os.path.join(script_dir, "cps21_imp_iss_value_counts.txt")

    # Write value counts to the file
    with open(output_file, "w") as f:
        f.write("Value counts for cps21_imp_iss:\n")
        f.write(value_counts.to_string())

    print(f"Value counts have been saved to {output_file}")

"""
# Create the output file path
output_file = os.path.join(script_dir, "vars.txt")

# Write variable names to vars.txt
with open(output_file, "w") as f:
    f.write("Variable names:\n")
    for var_name in df.columns:
        f.write(f"{var_name}\n")

print(f"Variable names have been saved to {output_file}")
"""
