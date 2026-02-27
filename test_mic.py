import pyaudio
import numpy as np
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3

p = pyaudio.PyAudio()

print(f"Recording for {RECORD_SECONDS} seconds...")
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    rms = np.sqrt(np.mean(np.frombuffer(data, dtype=np.int16).astype(float)**2))
    print(f"RMS: {rms:.2f}")
    frames.append(data)

print("Done recording.")
stream.stop_stream()
stream.close()
p.terminate()
