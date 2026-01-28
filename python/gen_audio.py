import numpy as np
import soundfile as sf
import os
from scipy.signal import firwin

# Get directory of THIS script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Resolving input path relative to script
input_wav_path = os.path.join(script_dir, "voice.wav")
output_txt_path = os.path.join(os.path.dirname(script_dir), "tb", "audio_input.txt")
config_fs_path = os.path.join(script_dir, "config_fs.txt")

# ===============================
# 1. Load audio file
# ===============================
try:
    audio, fs = sf.read(input_wav_path)
    print(f"Detected Sample Rate: {fs} Hz")

    # Save FS for recover_audio.py
    with open(config_fs_path, "w") as f:
        f.write(str(fs))
except Exception as e:
    print(f"Error loading {input_wav_path}: {e}")
    exit(1)


if audio.ndim > 1:
    audio = np.mean(audio, axis=1)

# ===============================
# 2. Add noise & Apply Stronger Gain
# ===============================
# noise = 0.01 * np.random.randn(len(audio)) 
noisy = audio # + noise
# Reduce gain to 0.9 to prevent clipping (1.8 was too high)
gain = 0.9 
amplified = noisy * gain

# ===============================
# 3. Custom FIR Coefficients (Manual Tuning)
# ===============================
# Instead of standard firwin (which is muffled), we use a 
# "Loudness Contour" set that emphasizes Bass (Taps 0,4) and Clarity (Tap 2)
# Copy these into your fir_core.v
coeff_int = np.array([2500, -1500, 10000, -1500, 2500])

print("--- COPY THESE INTO YOUR VERILOG fir_core.v ---")
for i, c in enumerate(coeff_int):
    # Fixed the minus sign syntax for Verilog
    if c < 0:
        print(f"coeff[{i}] = -16'sd{abs(c)};")
    else:
        print(f"coeff[{i}] = 16'sd{c};")
print("-----------------------------------------------")

# ===============================
# 4. Save for Verilog Testbench
# ===============================
# We send the RAW amplified audio to the FPGA. 
# The FPGA will perform the Filtering and Echo.
fixed_input = np.clip(amplified * 32767, -32768, 32767).astype(np.int16)

# Use robust path
np.savetxt(output_txt_path, fixed_input, fmt="%d")

print(f"\naudio_input.txt generated. Samples: {len(fixed_input)}")
print("Note: The FPGA will now add the Bass boost and Echo effect.")