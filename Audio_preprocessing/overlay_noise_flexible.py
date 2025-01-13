import os
import sys
import pandas as pd
import random
import numpy as np
from pydub import AudioSegment

def process_directory(owl_folder_path, noise_folder_path, output_folder_path):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # List all the owl and noise files
    owl_files = [f for f in os.listdir(owl_folder_path) if f.endswith('.wav') or f.endswith('.WAV')]
    noise_files = [f for f in os.listdir(noise_folder_path) if f.endswith('.wav') or f.endswith('.WAV')]

    # Loop through all owl files
    for owl_file in owl_files:
        # Load the owl audio
        owl_audio_path = os.path.join(owl_folder_path, owl_file)
        owl_audio = AudioSegment.from_wav(owl_audio_path)

        # Randomly select a noise file
        random_noise_file = random.choice(noise_files)
        noise_audio_path = os.path.join(noise_folder_path, random_noise_file)
        noise_audio = AudioSegment.from_wav(noise_audio_path)

        # Ensure the noise audio is at least as long as the owl audio
        if len(noise_audio) < len(owl_audio):
            noise_audio = noise_audio + noise_audio[:len(owl_audio) - len(noise_audio)]

        # Randomly choose an SNR value within the range 35-55 dB for this overlay
        snr_dB = random.uniform(35, 55)

        # Calculate the power ratio for the desired SNR
        snr_linear = 10 ** (snr_dB / 10.0)

        # Calculate the RMS (Root Mean Square) of the owl audio
        owl_rms = np.sqrt(np.mean(np.array(owl_audio.get_array_of_samples())**2))

        # Calculate the RMS of the noise audio
        noise_rms = np.sqrt(np.mean(np.array(noise_audio.get_array_of_samples())**2))

        # Calculate the adjusted RMS for the noise to achieve the desired SNR
        adjusted_noise_rms = owl_rms / np.sqrt(snr_linear)

        # Calculate the adjustment needed in dBFS
        adjustment_dBFS = 20 * np.log10(adjusted_noise_rms / (noise_rms if noise_rms > 0 else 1))

        # Apply the adjustment to the noise audio
        noise_audio = noise_audio.apply_gain(adjustment_dBFS - noise_audio.dBFS)

        # Overlay the owl audio with the adjusted noise
        combined_audio = owl_audio.overlay(noise_audio)

        # Save the overlayed audio to the output folder
        output_filename = f"overlaid_{owl_file}"
        output_path = os.path.join(output_folder_path, output_filename)
        combined_audio.export(output_path, format="wav")

    print(f"Noise overlay process with varying SNR completed for: {owl_folder_path}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python script_name.py <owl_folder_path> <noise_folder_path> <output_folder_path>")
        sys.exit(1)

    owl_folder_path = sys.argv[1]
    noise_folder_path = sys.argv[2]
    output_folder_path = sys.argv[3]

    for subdir, dirs, files in os.walk(owl_folder_path):
        for dir in dirs:
            process_directory(os.path.join(subdir, dir), noise_folder_path, os.path.join(output_folder_path, dir))
