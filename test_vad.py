from pita.backend.audio.vad import VADEngine
import numpy as np

print("Initializing VAD...")
vad = VADEngine()
print("VAD Initialized.")

# Dummy audio
dummy_audio = np.zeros(512, dtype=np.int16).tobytes()
print("Checking VAD...")
is_speech = vad.is_speech(dummy_audio)
print(f"Result: {is_speech}")
