import pyaudio

p = pyaudio.PyAudio()
print(f"Default Input Device: {p.get_default_input_device_info()['name']}")
print("\nAll Input Devices:")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        print(f"Index {i}: {info['name']} (Channels: {info['maxInputChannels']}, SampleRate: {info['defaultSampleRate']})")
p.terminate()
