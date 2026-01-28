import soundfile as sf
audio, fs = sf.read("input.wav")
print(f"Sample Rate: {fs}")
print(f"Samples: {len(audio)}")
print(f"Duration: {len(audio)/fs:.2f} seconds")
