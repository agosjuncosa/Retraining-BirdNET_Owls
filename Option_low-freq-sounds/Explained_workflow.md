# Improving BirdNET Detection for Low-Pitch Songs

## **📌 Overview**
In each iteration of active learning, I compute:
- **Macro mAP** for all classes.
- **AP (Average Precision) curves per class**.
- **A table tracking per-class mAP values across iterations** to monitor model improvement.

### **Low-Frequency Species of Interest**
BirdNET struggles with species that have low frequency. Some owl species have their **dominant frequency bands below 500 Hz**. These include:

#### **🦉 Species with low-pitch songs but a high pitch call:**
- Mottled Owl (*Strix virgata*) – song & call
- Striped Owl (*Asio clamator*) – song & call
- Stygian Owl (*Asio stygius*) – song & call
- Rusty-barred Owl (*Strix hylophila*) – song & call

#### **🦉 Species with predominantly low-pitch songs:**
- Tawny-browed Owl (*Pulsatrix koeniswaldiana*)
- Black-banded Owl (*Strix huhula*)

These species have dominant frequencies between **100-400 Hz**, making them difficult for BirdNET, which performs best on **mid-to-high frequency vocalizations**.

---

## **🔹 Strategy for Enhancing Low-Frequency Detection**
If BirdNET fails to detect these low-pitch species during active learning, I will experiment with **two alternative approaches**:

### **1️⃣ BirdNET Model A: Bandpass Filter (0-3000 Hz)**
📌 **Goal:** Improve detection by removing high frequencies that dominate the spectrogram.

📌 **Steps:**
- **Fine-tune BirdNET** using a **bandpass filter (0-3000 Hz)** during training:
  ```sh
  python -m birdnet_analyzer.train /path/to/training_data --fmin 0 --fmax 3000
  ```
- **Analyze field data** using the **same frequency range**:
  ```sh
  python -m birdnet_analyzer.analyze /path/to/unlabeled_data --fmin 0 --fmax 3000
  ```

📌 **Expected Outcome:**
- The model should **better capture low-frequency energy**.
- May **reduce false positives from high-frequency bird calls**.

---

### **2️⃣ BirdNET Model B: Upsampled Data (Pitch-Shifted)**
📌 **Goal:** Shift low-frequency sounds **into a higher frequency range (1-2 kHz)** where BirdNET performs better.

📌 **Steps:**
- **Apply pitch shift (upsampling) to training data** before training:
  ```python
  import librosa
  import soundfile as sf
  
  def upsample_audio(filename, n_steps=24):  # Default to 2 octaves
      y, sr = librosa.load(filename, sr=None)
      y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=n_steps)
      sf.write(filename.replace(".wav", "_upsampled.wav"), y_shifted, sr)
  
  # Example Usage:
  upsample_audio("low_freq_species.wav", n_steps=24)  # Shift 2 octaves
  ```
- **Fine-tune BirdNET** using the upsampled data:
  ```sh
  python -m birdnet_analyzer.train /path/to/upsampled_training_data
  ```
- **Analyze field data** by first applying the same pitch shift:
  ```sh
  python -m birdnet_analyzer.analyze /path/to/upsampled_unlabeled_data
  ```

📌 **Expected Outcome:**
- Low-frequency calls should **appear higher** in the spectrogram.
- May improve BirdNET’s ability to **differentiate target low-frequency sounds from background noise**.

---

## **🚀 Conclusion & Next Steps**
1. **Run BirdNET on unmodified data** to confirm low-frequency detection issues.
2. **Test both approaches (Model A & Model B) on the same dataset**.
3. **Compare precision & recall** to determine which method is more effective.
4. If neither model is sufficient, consider **additional fine-tuning strategies**.

🎯 **This strategy will help improve detection of low-pitch owl songs and refine BirdNET's classification ability!** 🦉🔥