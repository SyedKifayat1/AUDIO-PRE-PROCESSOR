import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import os

# Get directory of THIS script
script_dir = os.path.dirname(os.path.abspath(__file__))
input_wav_path = os.path.join(script_dir, "input.wav")
output_wav_path = os.path.join(os.path.dirname(script_dir), "output", "recovered_audio.wav")

def plot_comparison():
    try:
        # Load Files
        data_in, fs_in = sf.read(input_wav_path)
        data_out, fs_out = sf.read(output_wav_path)
        
        # Handle stereo input (take one channel)
        if data_in.ndim > 1:
            data_in = np.mean(data_in, axis=1)
            
        # Truncate to matching lengths for comparison
        min_len = min(len(data_in), len(data_out))
        data_in = data_in[:min_len]
        data_out = data_out[:min_len]

        # Setup Plot
        fig, axs = plt.subplots(3, 1, figsize=(10, 12))
        
        # 1. Waveform Comparison
        axs[0].plot(data_in, label='Input (Original)', alpha=0.7)
        axs[0].plot(data_out, label='Output (Processed)', alpha=0.7)
        axs[0].set_title("Waveform Overlay")
        axs[0].legend()
        
        # 2. Input Spectrogram
        axs[1].specgram(data_in, Fs=fs_in, NFFT=1024, cmap='viridis')
        axs[1].set_title("Input Spectrogram")
        axs[1].set_ylabel("Frequency (Hz)")

        # 3. Output Spectrogram
        axs[2].specgram(data_out, Fs=fs_out, NFFT=1024, cmap='magma')
        axs[2].set_title("Output Spectrogram (Look for filtering effects)")
        axs[2].set_ylabel("Frequency (Hz)")

        plt.tight_layout()
        print("Displaying comparison plot...")
        plt.show()

    except Exception as e:
        print(f"Error during comparison: {e}")

if __name__ == "__main__":
    plot_comparison()
