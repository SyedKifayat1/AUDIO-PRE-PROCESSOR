import os

# Coefficients for Passthrough (No Filtering)
# We set the center tap to 1 (scaled) and others to 0.
# This makes the FIR filter "transparent".
center_tap = 16384 # 0.5 to leave headroom for Echo addition

verilog_content = f"""
        2'b00, 2'b01, 2'b10: begin // PASSTHROUGH (Echo Only Test)
            coeff[0] = 16'sd0;
            coeff[1] = 16'sd0;
            coeff[2] = 16'sd{center_tap};
            coeff[3] = 16'sd0;
            coeff[4] = 16'sd0;
        end
"""

fir_core_path = r"E:\GitHub Data\AUDIO-PRE-PROCESSOR\rtl\fir_core.v"

print("Setting up Echo Isolation Test...")

# We read the file, and replace the case statement logic 
# This is a bit brute force but effective for a quick test script
with open(fir_core_path, "r") as f:
    lines = f.readlines()

new_lines = []
in_always_block = False
replaced = False

for line in lines:
    if "always @(*)" in line:
        in_always_block = True
        new_lines.append(line)
        continue
    
    if in_always_block and "endcase" in line:
        in_always_block = False
        new_lines.append(verilog_content) # Insert our override
        new_lines.append(line)
        replaced = True
        continue
        
    if in_always_block:
        pass # Skip existing logic
    else:
        new_lines.append(line)

# For safety, manual instructions are better than risky regex replacement
print("\n" + "="*50)
print("       MANUAL STEP REQUIRED FOR ECHO TEST")
print("="*50)
print("To hear ONLY the echo, we must disable the Bass/Treble filters.")
print("Open 'rtl/fir_core.v' and change the coefficients for the current mode to:")
print(f"coeff[0] = 0;")
print(f"coeff[1] = 0;")
print(f"coeff[2] = 16384;")
print(f"coeff[3] = 0;")
print(f"coeff[4] = 0;")
print("\nThen Relaunch Simulation.")
print("="*50)
