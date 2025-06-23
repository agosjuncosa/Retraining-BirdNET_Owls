import os
import shutil
import random
import argparse
from pathlib import Path

# Load previously used filenames from the list file
def load_used_filenames(selection_path):
    with open(selection_path, "r") as f:
        return set(os.path.basename(line.strip()) for line in f if line.strip())

# Define night periods
night_periods = {
    'Late_night': ['000000', '033000'],
    'Dawn': ['034000', '071000'],
    'Dusk': ['180000', '213000'],
    'Night': ['214000', '235000']
}

# Check if a time string belongs to a given period
def is_within_period(time_str, period):
    start, end = night_periods[period]
    return start <= time_str <= end

# Find all night_recordings folders inside Disco*_Backup
def find_night_recording_dirs(root_dir):
    night_dirs = []
    root_path = Path(root_dir)
    for disco in root_path.glob("Disco*_Backup"):
        for subdir in disco.rglob("night_recordings"):
            if subdir.is_dir():
                night_dirs.append(subdir)
    return night_dirs

def stratified_selection_excluding_used(root_dir, target_dir, used_set):
    night_recording_dirs = find_night_recording_dirs(root_dir)

    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)

    any_file_copied = False  # Track if any files were copied

    for night_dir in night_recording_dirs:
        for site in os.listdir(night_dir):
            site_dir = os.path.join(night_dir, site)
            if os.path.isdir(site_dir):
                clips_per_period = 95 if site.startswith('M') else 80
                period_files = {period: [] for period in night_periods}

                for survey_night in os.listdir(site_dir):
                    sn_dir = os.path.join(site_dir, survey_night)
                    if os.path.isdir(sn_dir):
                        for audio_file in os.listdir(sn_dir):
                            if audio_file.lower().endswith('.wav') and audio_file not in used_set:
                                time_part = audio_file.split('_')[-1][:6]
                                for period in night_periods:
                                    if is_within_period(time_part, period):
                                        period_files[period].append(os.path.join(sn_dir, audio_file))

                for period in period_files:
                    selected = random.sample(period_files[period], min(clips_per_period, len(period_files[period])))
                    for file_path in selected:
                        shutil.copy(file_path, target_dir)
                        any_file_copied = True

    if any_file_copied:
        print("New subset created, excluding previously used recordings.")
    else:
        print("No new files were copied. Check if any eligible files remain.")

# Script entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root_dir", type=str, help="Top-level root directory (e.g., /mnt/d/)")
    parser.add_argument("target_dir", type=str, help="Target folder to copy new subset")
    parser.add_argument("used_list", type=str, help=".txt file listing previously used files")
    args = parser.parse_args()

    used_files = load_used_filenames(args.used_list)
    stratified_selection_excluding_used(args.root_dir, args.target_dir, used_files)
