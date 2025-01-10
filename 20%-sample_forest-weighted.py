#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import shutil
import random
import argparse

# Define the night periods and their corresponding time ranges
night_periods = {
    'Late_night': ['000000', '033000'],
    'Dawn': ['034000', '071000'],
    'Dusk': ['180000', '213000'],
    'Night': ['214000', '235000']
}

# Function to check if a time string is within a specific period
def is_within_period(time_str, period):
    start, end = night_periods[period]
    return start <= time_str <= end

# Main function to perform the stratified selection
def stratified_selection(root_dir, target_dir):
    # Loop through each site directory
    for site in os.listdir(root_dir):
        site_dir = os.path.join(root_dir, site)
        if os.path.isdir(site_dir):
            # Determine the habitat type based on the site folder name
            if site.startswith('M'):  # Forest
                clips_per_period = 95
            else:  # Farms (CH) or Pine Plantations (P)
                clips_per_period = 80

            # Initialize a dictionary to store files for each night period
            period_files = {period: [] for period in night_periods}

            # Loop through each survey night directory within the site
            for survey_night in os.listdir(site_dir):
                sn_dir = os.path.join(site_dir, survey_night)
                if os.path.isdir(sn_dir):
                    # Loop through each audio file within the survey night directory
                    for audio_file in os.listdir(sn_dir):
                        if audio_file.lower().endswith('.wav'):
                            # Extract the time part from the audio file name
                            time_part = audio_file.split('_')[-1][:6]  # The [-1] selects the last substring of the filename
                            # Check which period the time part belongs to and add to the respective list
                            for period in night_periods:
                                if is_within_period(time_part, period):
                                    period_files[period].append(os.path.join(sn_dir, audio_file))

            # Randomly select files from each period and copy them to the target directory
            for period in period_files:
                # Select the specified number of files or fewer if not enough available
                selected_files = random.sample(period_files[period], min(clips_per_period, len(period_files[period])))
                for file_path in selected_files:
                    shutil.copy(file_path, target_dir)

    print("Files have been successfully copied to the target directory.")

# Argument parser for running the script from the console
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stratified selection of audio files based on habitat type and night periods.")
    parser.add_argument("root_dir", type=str, help="Root directory containing the site folders.")
    parser.add_argument("target_dir", type=str, help="Target directory to store the selected audio files.")
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    stratified_selection(args.root_dir, args.target_dir)

