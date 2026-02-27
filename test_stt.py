from pita.backend.audio.stt import STTEngine
import numpy as np

print("Initializing STT...", flush=True)
stt = STTEngine()
print("STT Initialized.", flush=True)

# Dummy audio
dummy_audio = np.zeros(16000, dtype=np.int16).tobytes()
print("Transcribing dummy audio...", flush=True)
text = stt.transcribe(dummy_audio)
print(f"Result: '{text}'", flush=True)
