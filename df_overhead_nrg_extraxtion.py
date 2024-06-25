#!/usr/bin/env python3

"""Run ns-3 simulation campaign using SEM (Simulation Execution manager).

Defines the wrapper functions to configure and run simulation campaigns.
Currently focuses on performing multiple runs with the same set of provided params.
"""

import sem
import pprint
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
sns.set_style("white")

if not os.path.exists("overhead-nrg/"):
    os.makedirs("overhead-nrg/")

def parse_file(file):
    try:
        # Extract data from the output file
        stdout = file['output']['ovrhead-nrg.log']
        numbers = [float(num.strip()) for num in stdout.split(',') if num.strip()]

        # Ensure the numbers list has the expected number of elements
        if len(numbers) < 6:
            raise ValueError(f"Unexpected format: {numbers}")

        # Parse each component
        communication_link = ["Up Link", "Down Link", "Duplex"][int(numbers[1]) - 1]
        power_save_mechanism = ["PSM", "TWT", "Active"][int(numbers[1]) - 1]
        generated_traffic = ["Periodic", "Poisson", "Full Buffer"][int(numbers[2]) - 1]
        transport_protocol = ["TCP", "UDP"][int(numbers[3])]
        packets_per_second = numbers[4]
        sta_count = int(numbers[5])
        sta_overhead = numbers[-2]
        ap_overhead = numbers[-1]
        # Return parsed data as a list
        return [communication_link, power_save_mechanism, generated_traffic,
                transport_protocol, packets_per_second, sta_count,
                sta_overhead, ap_overhead]
    except ValueError as e:
        print(f"Error parsing file: {e}")
        print(f"File content: {stdout}")
        return None
    except IndexError as e:
        print(f"Index error: {e}")
        print(f"File content: {stdout}")
        return None

# Load the simulation campaign
campaign_dir = "test1"
campaign = sem.CampaignManager.load(campaign_dir)

# Retrieve complete results from the campaign database
results = campaign.db.get_complete_results()

# Parse pcktloss data for each result and store it in a list of lists
parsed_data = [parse_file(result) for result in results]
parsed_data = [data for data in parsed_data if data is not None]

# Define column names for the DataFrame
column_names = ['Communication_link', 'Power_save_mechanism', 'Generated_traffic',
                'Transport_protocol', 'Packets_per_second', 'Sta_count',
                'sta_overhead', 'ap_overhead']

# Create a DataFrame from the parsed data
overhead_df = pd.DataFrame(parsed_data, columns=column_names)
overhead_df.to_csv(os.path.join("overhead-nrg", "overhead_df.csv"), index=False)
# Print or further process the DataFrame as needed
print(overhead_df.head(10))