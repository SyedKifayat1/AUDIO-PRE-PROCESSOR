# python/verify_output.py
import numpy as np
import matplotlib.pyplot as plt

inp = np.loadtxt("../tb/audio_input.txt")
out = np.loadtxt("../output/vivado_output.txt")

plt.figure(figsize=(10,4))
plt.plot(inp[:500], label="Input")
plt.plot(out[:500], label="Processed")
plt.legend()
plt.title("Audio Preprocessor Verification")
plt.show()
