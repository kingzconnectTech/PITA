import pyaudio
import numpy as np

p = pyaudio.PyAudio()
CHUNK = 1024
RATE = 16000

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        print(f"\nTesting Index {i}: {info['name']}")
        try:
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=RATE,
                            input=True,
                            input_device_index=i,
                            frames_per_buffer=CHUNK)
            
            # Read 5 chunks
            total_rms = 0
            for _ in range(5):
                data = stream.read(CHUNK, exception_on_overflow=False)
                rms = np.sqrt(np.mean(np.frombuffer(data, dtype=np.int16).astype(float)**2))
                total_rms += rms
            
            avg_rms = total_rms / 5
            print(f"  Average RMS: {avg_rms:.2f}")
            stream.stop_stream()
            stream.close()
        except Exception as e:
            print(f"  Failed: {e}")

p.terminate()
