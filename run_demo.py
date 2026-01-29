import os
import time

def main():
    print("========================================")
    print("      Audio Pre-Processor Demo          ")
    print("========================================")
    print("Select Filter Mode:")
    print("  0: Bass (Low Pass)")
    print("  1: Treble (High Pass)")
    print("  2: Bandpass (Voice Clarity)")
    
    while True:
        try:
            selection = int(input("\nEnter your choice (0, 1, or 2): "))
            if selection in [0, 1, 2]:
                break
            print("Invalid input. Please enter 0, 1, or 2.")
        except ValueError:
            print("Please enter a number.")

    # Write selection to the file that Testbench reads
    # Using absolute path to match the testbench configuration
    tb_config_path = r"E:\GitHub Data\AUDIO-PRE-PROCESSOR\tb\filter_mode.txt"
    with open(tb_config_path, "w") as f:
        f.write(str(selection))
    
    print(f"\n[OK] Mode {selection} set.")
    print("----------------------------------------")
    print("Step 1: Generating Input Audio...")
    os.system("python python/gen_audio.py")
    
    print("----------------------------------------")
    print("Step 2: RUN VIVADO SIMULATION NOW")
    print("Go to Vivado -> Click 'Relaunch Simulation' -> Wait for finish.")
    input("Press Enter continue once Simulation is DONE...")
    
    print("----------------------------------------")
    print("Step 3: Recovering Output Audio...")
    os.system("python python/recover_audio.py")

    print("----------------------------------------")
    print("Step 4: Visualizing Results...")
    os.system("python python/compare_audio.py")
    
    print("\n========================================")
    print("Done! Check 'output/recovered_audio.wav'")
    print("========================================")

if __name__ == "__main__":
    main()
