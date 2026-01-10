import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

# ===============================
# 1. Configuration
# ===============================
SAMPLE_RATE = 44100 
INPUT_PATH = "E:/GitHub Data/AUDIO-PRE-PROCESSOR/output/vivado_output.txt"
OUTPUT_WAV = "E:/GitHub Data/AUDIO-PRE-PROCESSOR/output/recovered_audio.wav"

try:
    # ===============================
    # 2. Load Vivado Output
    # ===============================
    # We use 'ndmin=1' to prevent errors if the file is very short
    vivado_data = np.loadtxt(INPUT_PATH, ndmin=1)

    if vivado_data.size == 0:
        raise ValueError("The output file is empty. Did you 'run all' in Vivado?")

    # ===============================
    # 3. Normalize & Quality Check
    # ===============================
    # Convert from 16-bit signed integer back to float (-1.0 to 1.0)
    recovered_audio = vivado_data / 32768.0

    # Final Safety Clip (Crucial for the 'Loudness' boost)
    recovered_audio = np.clip(recovered_audio, -1.0, 1.0)

    # ===============================
    # 4. Save and Analyze
    # ===============================
    sf.write(OUTPUT_WAV, recovered_audio.astype(np.float32), SAMPLE_RATE)
    print(f"File recovered successfully: {OUTPUT_WAV}")
    print(f"Total samples processed: {len(recovered_audio)}")

    # Plotting: We will plot two views
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # View 1: The waveform (Time Domain)
    ax1.plot(recovered_audio)
    ax1.set_title("Full Recovered Audio (With Echo Tail)")
    ax1.set_ylabel("Amplitude")

    # View 2: Spectrogram (Frequency Domain - Required for your project!)
    # This proves your Bass and Clarity boost worked
    ax2.specgram(recovered_audio, Fs=SAMPLE_RATE, NFFT=1024, cmap='magma')
    ax2.set_title("Audio Spectrogram (Visual Proof of Filtering)")
    ax2.set_ylabel("Frequency (Hz)")
    ax2.set_xlabel("Time (s)")

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Error: {e}")