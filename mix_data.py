import pandas as pd

# Read 'delay_df.csv' file
delay_df = pd.read_csv('delay/delay_df.csv')
# Read 'pcktloss_df.csv' and 'thrpt_df.csv' files
pcktloss_df = pd.read_csv('pcktloss/pcktloss_df.csv')
thrpt_df = pd.read_csv('thrpt/thrpt_df.csv')
nrg_df = pd.read_csv('nrg/nrg_df.csv')
overhead_df = pd.read_csv('overhead-nrg/overhead_df.csv')
# Select the last two columns from 'pcktloss_df' and 'thrpt_df'
pcktloss_last_two = pcktloss_df.iloc[:, -2:]
thrpt_last_two = thrpt_df.iloc[:, -2:]
nrg_last_two = nrg_df.iloc[:, -2:]
overhead_last_two = overhead_df.iloc[:, -2:]


# Append the last two columns to 'delay_df'
all_df = pd.concat([delay_df, pcktloss_last_two, thrpt_last_two, nrg_last_two, overhead_last_two], axis=1)

print(all_df.head(20))

# Save the combined DataFrame to a new CSV file
all_df.to_csv('combined_data.csv', index=False)
