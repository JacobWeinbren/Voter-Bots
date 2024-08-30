import pyreadstat
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data", "2022.sav")

# Read the .sav file
df, meta = pyreadstat.read_sav(file_path)

# Print all variable names
print("Variable names:")
for var_name in df.columns:
    print(var_name)

# Print the values of v143_code
print("\nValues of v143_code:")
print(df["v8_code1"].tolist())
