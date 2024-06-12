import pandas as pd

# Load the CSV files into DataFrames
iss_df = pd.read_csv('data_source/MCDB_clean_iss_2024-05-17_09_42_05.csv')
ret_df = pd.read_csv('data_source/MCDB_clean_ret_2024-05-17_09_42_05.csv')

# Print columns to check available data
print("Columns in ISS DataFrame:", iss_df.columns)
print("Columns in RET DataFrame:", ret_df.columns)