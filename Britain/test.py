import pyreadstat
import os

# Get the current script's directory
current_location = os.path.dirname(os.path.abspath(__file__))

# Read the SPSS file
df, meta = pyreadstat.read_sav(os.path.join(current_location, "data", "BES.sav"))

# Print all variable names
print("Variables in the SPSS file:")
for variable in df.columns:
    print(variable)

# Print new_pcon_codeW29
print("\nnew_pcon_codeW29:")
print(df["new_pcon_codeW29"])
