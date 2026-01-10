import numpy as np
import soundfile as sf
from scipy.signal import firwin

# ===============================
# 1. Load audio file
# ===============================
audio, fs = sf.read("input.wav")

if audio.ndim > 1:
    audio = np.mean(audio, axis=1)

# ===============================
# 2. Add noise & Apply Stronger Gain
# ===============================
noise = 0.01 * np.random.randn(len(audio)) 
noisy = audio + noise
# Increase gain to 1.8 for "Louder" signal. 
# Your Verilog Saturation logic will handle any peaks.
gain = 1.8 
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
np.savetxt("../tb/audio_input.txt", fixed_input, fmt="%d")

print(f"\naudio_input.txt generated. Samples: {len(fixed_input)}")
print("Note: The FPGA will now add the Bass boost and Echo effect.")