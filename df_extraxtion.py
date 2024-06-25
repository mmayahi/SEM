import os
import sem
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("white")

# Create directories if they don't exist
if not os.path.exists("delay/"):
    os.makedirs("delay/")

def parse_file(file):
    """
    Parse delay data from the output file of the simulation.
    """
    # Extract data from the output file
    stdout = file['output']['dlay.log']

    # Filter out empty strings and convert to float
    try:
        numbers = [float(num.strip()) for num in stdout.split(',') if num.strip()]
    except ValueError as e:
        print(f"Error parsing numbers from stdout: {e}")
        return None

    # Ensure there are enough numbers to parse
    if len(numbers) < 8:
        print("Not enough data to parse. Skipping this entry.")
        return None

    # Parse each component
    if numbers[0] == 1:
        communication_link = "Up Link"
        uplink_delay = numbers[6]
        downlink_delay = 0
    elif numbers[0] == 2:
        communication_link = "Down Link"
        uplink_delay = 0
        downlink_delay = numbers[7]
    elif numbers[0] == 3:
        communication_link = "Duplex"
        uplink_delay = numbers[6]
        downlink_delay = numbers[7]

    power_save_mechanism = ["PSM", "TWT", "Active"][int(numbers[1]) - 1]
    generated_traffic = ["Periodic", "Poisson", "Full Buffer"][int(numbers[2]) - 1]
    transport_protocol = ["TCP", "UDP"][int(numbers[3])]
    packets_per_second = numbers[4]
    sta_count = int(numbers[5])

    # Initialize list for station distances
    sta_distances = []
    for i in range(6, 6 + sta_count):
        if i < len(numbers):
            sta_distances.append(numbers[i])
        else:
            sta_distances.append(None)

    # Return parsed data as a list
    return [communication_link, power_save_mechanism, generated_traffic,
            transport_protocol, packets_per_second, sta_count, sta_distances,
            uplink_delay, downlink_delay]

# Load the simulation campaign
campaign_dir = "test1"
campaign = sem.CampaignManager.load(campaign_dir)

# Retrieve complete results from the campaign database
results = campaign.db.get_complete_results()

# Parse delay data for each result and store it in a list of lists
parsed_data = []
max_sta_count = 0
for result in results:
    parsed_result = parse_file(result)
    if parsed_result:
        parsed_data.append(parsed_result)
        max_sta_count = max(max_sta_count, parsed_result[5])

# Define column names for the DataFrame
base_column_names = ['Communication_link', 'Power_save_mechanism', 'Generated_traffic',
                     'Transport_protocol', 'Packets_per_second', 'Sta_count']

# Dynamically add station distance column names
sta_distance_columns = [f'Sta_distance{i+1}' for i in range(max_sta_count)]
column_names = base_column_names + sta_distance_columns + ['Uplink_delay', 'Downlink_delay']

# Create a DataFrame from the parsed data
df_rows = []
for data in parsed_data:
    base_data = data[:6]  # Base data excluding station distances
    sta_distances = data[6]  # Station distances
    uplink_delay = data[7]  # Uplink delay
    downlink_delay = data[8]  # Downlink delay
    
    # Pad sta_distances with None to match max_sta_count
    sta_distances += [None] * (max_sta_count - len(sta_distances))
    
    # Concatenate each station distance individually to the base data
    row = base_data + sta_distances + [uplink_delay, downlink_delay]
    df_rows.append(row)

# Create DataFrame with the updated column names
delay_df = pd.DataFrame(df_rows, columns=column_names)
delay_df.to_csv(os.path.join("delay", "delay_df.csv"), index=False)
# Print or further process the DataFrame as needed
print(delay_df.head())

# Group the DataFrame by specified parameters and aggregate the data
grouped_data = delay_df.groupby(['Communication_link', 'Power_save_mechanism', 'Generated_traffic', 'Transport_protocol', 'Packets_per_second'])

# Plot the data
#sns.set_style("whitegrid")
#if not os.path.exists("plots2/delay_plots"):
#    os.makedirs("plots2/delay_plots")

#for group_name, group_data in grouped_data:
#    plt.figure(figsize=(8, 6))
#    sns.lineplot(data=group_data, x='Sta_count', y='Uplink_delay', label='Uplink_delay')
#    sns.lineplot(data=group_data, x='Sta_count', y='Downlink_delay', label='Downlink_delay')
#    plt.title(f"{', '.join(group_name[:-1])}, {group_name[-1]} PPS")
#    plt.xlabel("Sta_count")
#   plt.ylabel("Delay (ms)")
#   plt.xticks([1, 2, 3])  # Set the ticks on x-axis to be 1, 2, 3
#   plt.legend()
#   filepath = os.path.join("plots2/delay_plots", f"{'_'.join(map(str, group_name))}.png")
#   plt.savefig(filepath)
#   plt.close()  # Close the current figure to free up memory
#lse:
#   print("No valid data parsed from the results.")
#