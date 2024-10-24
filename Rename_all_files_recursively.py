#!/usr/bin/env python
# coding: utf-8

import os
import argparse

def rename_files(base_path):
    # Loop through each directory in the base directory
    for site_long_id in os.listdir(base_path):
        site_path = os.path.join(base_path, site_long_id)
        # Extract only the first part of the long id
        site_id = site_long_id.split('-')[0]
        # Check if the current path is a directory
        if os.path.isdir(site_path):
            # Loop through each sampling occasion within the site directory
            for sn in os.listdir(site_path):
                sn_path = os.path.join(site_path, sn)
                if os.path.isdir(sn_path) and sn.startswith('SN'):
                    # Loop through each .wav file within the sampling occasion directory
                    for filename in os.listdir(sn_path):
                        if filename.endswith('.WAV'):
                            old_file_path = os.path.join(sn_path, filename)
                            
                            # Check if the file is already renamed by checking if it starts with site_id
                            if filename.startswith(site_id):
                                print(f"Skipping already renamed file: {filename}")
                                continue
                            
                            # Construct the new filename (e.g., P26_SN06_20220801_183000.WAV)
                            new_filename = f"{site_id}_{sn.replace('_', '')}_{filename}"
                            new_file_path = os.path.join(sn_path, new_filename)
                            
                            # Rename the file
                            os.rename(old_file_path, new_file_path)
                            print(f"Renamed {old_file_path} to {new_file_path}")

if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Rename .WAV files in a directory based on folder structure.")
    
    # Add argument for input path
    parser.add_argument("--i", required=True, help="Path to the base directory containing all the site folders")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call the rename_files function with the provided path
    rename_files(args.i)




