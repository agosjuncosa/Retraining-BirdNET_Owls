#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import shutil
import random
import argparse

# Function to check if a time string is within a specific period
def is_within_period(time_str, period, night_periods):
    start, end = night_periods[period]
    if start <= time_str <= end:
        return True
    return False

def main(input_dir, output_dir):
    # Define the night periods and their corresponding time ranges
    night_periods = {
        'Late_night': ['000000', '033000'],
        'Dawn': ['034000', '071000'],
        'Dusk': ['180000', '213000'],
        'Night': ['214000', '235000']
    }
    
    # Loop through each site directory
    for site in os.listdir(input_dir):
        site_dir = os.path.join(input_dir, site)
        if os.path.isdir(site_dir):
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
                            time_part = audio_file.split('_')[-1][:6]
                            # Check which period the time part belongs to and add to the respective list
                            for period in night_periods:
                                if is_within_period(time_part, period, night_periods):
                                    period_files[period].append(os.path.join(sn_dir, audio_file))
            
            # Randomly select 41 files from each period and copy them to the target directory
            for period in period_files:
                selected_files = random.sample(period_files[period], min(41, len(period_files[period])))
                for file_path in selected_files:
                    shutil.copy(file_path, output_dir)

    print("Files have been successfully copied to the target directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract audio files based on time periods.')
    parser.add_argument('input_dir', type=str, help='The input directory containing night recordings.')
    parser.add_argument('output_dir', type=str, help='The output directory to store the extracted files.')
    args = parser.parse_args()

    main(args.input_dir, args.output_dir)

