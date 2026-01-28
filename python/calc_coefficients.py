import numpy as np
from scipy.signal import firwin

def to_fixed_point(coeffs, width=16):
    # Scale to fill range, but leave headroom
    # Max value for 16-bit signed is 32767
    # We sum 5 taps. If all are 1 and input is max, we overflow. 
    # But usually impulse response sum is ~1 (gain).
    # Let's scale so sum of absolute coeffs is close to 32767 for max dynamic range without overflow
    
    # Standard Q15 format: 1.0 = 32768
    scale = 32768.0
    
    fixed = np.round(coeffs * scale).astype(int)
    return fixed

def print_verilog(name, coeffs):
    print(f"// {name}")
    for i, c in enumerate(coeffs):
        if c < 0:
            print(f"coeff[{i}] = -16'sd{abs(c)};")
        else:
            print(f"coeff[{i}] = 16'sd{c};")
    print("")

fs = 48000 # Standard Audio
taps = 5

# 1. Bass (Low Pass) - Cutoff 400Hz
# 5 taps is very short for a sharp filter, so it will be a gentle slope
bass_coeffs = firwin(taps, cutoff=1000, fs=fs, pass_zero=True)
bass_fixed = to_fixed_point(bass_coeffs)

# 2. Treble (High Pass) - Cutoff 2000Hz
# firwin with pass_zero=False for High Pass
treble_coeffs = firwin(taps, cutoff=4000, fs=fs, pass_zero=False)
treble_fixed = to_fixed_point(treble_coeffs)

# 3. Bandpass (Mid) - Focus on 2kHz center
# With only 5 taps, a narrow 1k-4k bandpass is hard.
# We will design a "Mid High" filter (High Pass > 1kHz) to ensure it blocks Bass.
mid_coeffs = firwin(taps, cutoff=2000, fs=fs, pass_zero=False)
mid_fixed = to_fixed_point(mid_coeffs)


with open("coeffs_out.txt", "w") as f:
    f.write(f"// Calculated Coefficients for Fs={fs}Hz, Taps={taps}\n")
    
    def write_verilog(name, coeffs):
        f.write(f"// {name}\n")
        for i, c in enumerate(coeffs):
            if c < 0:
                f.write(f"coeff[{i}] = -16'sd{abs(c)};\n")
            else:
                f.write(f"coeff[{i}] = 16'sd{c};\n")
        f.write("\n")

    write_verilog("Mode 0: Bass (Low Pass < 1kHz)", bass_fixed)
    write_verilog("Mode 1: Treble (High Pass > 4kHz)", treble_fixed)
    write_verilog("Mode 2: Bandpass (1kHz - 4kHz)", mid_fixed)

print("Done writing to coeffs_out.txt")

