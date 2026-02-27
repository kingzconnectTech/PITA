import logging
import asyncio
import numpy as np
import pyaudio
from pita.backend.config.settings import SAMP_RATE, CHANNELS, INPUT_DEVICE_INDEX

logger = logging.getLogger("Lucy-Recorder")

class AudioRecorder:
    """
    Handles microphone capture.
    Provides chunks for VAD and STT.
    """
    def __init__(self):
        self.rate = SAMP_RATE
        self.channels = CHANNELS
        self.device_index = INPUT_DEVICE_INDEX
        self.chunk_size = 512
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.is_active = False
        
        # Log default device
        try:
            default_info = self.pa.get_default_input_device_info()
            logger.info(f"Default Audio Device: {default_info['name']} (Index: {default_info['index']})")
        except:
            logger.warning("No default input device found.")

        logger.info(f"Audio Recorder initialized at {self.rate}Hz")

    def start(self):
        """Starts the PyAudio stream."""
        if self.stream is not None:
            return
            
        target_index = self.device_index
        if target_index is None:
            try:
                target_index = self.pa.get_default_input_device_info()["index"]
            except:
                target_index = None
        used_index = target_index
        max_ch = None
        if used_index is not None:
            info = self.pa.get_device_info_by_index(used_index)
            max_ch = int(info.get("maxInputChannels", 1))
        else:
            info = self.pa.get_default_input_device_info()
            used_index = info["index"]
            max_ch = int(info.get("maxInputChannels", 1))
        ch = self.channels
        if max_ch and ch > max_ch:
            ch = max_ch
        if ch < 1:
            ch = 1
        try:
            self.stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=ch,
                rate=self.rate,
                input=True,
                input_device_index=used_index,
                frames_per_buffer=self.chunk_size
            )
            self.channels = ch
            self.is_active = True
            logger.info(f"Microphone stream started (Device Index: {used_index}, Channels: {self.channels}).")
        except Exception as e1:
            try:
                alt_ch = 2 if ch == 1 else 1
                self.stream = self.pa.open(
                    format=pyaudio.paInt16,
                    channels=alt_ch,
                    rate=self.rate,
                    input=True,
                    input_device_index=used_index,
                    frames_per_buffer=self.chunk_size
                )
                self.channels = alt_ch
                self.is_active = True
                logger.info(f"Microphone stream started after fallback (Device Index: {used_index}, Channels: {self.channels}).")
            except Exception as e2:
                try:
                    default_info = self.pa.get_default_input_device_info()
                    default_index = default_info["index"]
                    default_max = int(default_info.get("maxInputChannels", 1))
                    default_ch = min(default_max or 1, 2)
                    self.stream = self.pa.open(
                        format=pyaudio.paInt16,
                        channels=default_ch,
                        rate=self.rate,
                        input=True,
                        input_device_index=default_index,
                        frames_per_buffer=self.chunk_size
                    )
                    self.channels = default_ch
                    self.is_active = True
                    logger.info(f"Microphone stream started on default device (Index: {default_index}, Channels: {self.channels}).")
                except Exception as e3:
                    logger.error(f"Failed to start microphone stream: {e3}")
                    raise e3

    def stop(self):
        """Stops the PyAudio stream."""
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.is_active = False
        logger.info("Microphone stream stopped.")

    async def read_chunk(self):
        """Reads a single chunk of audio data from the stream."""
        if self.stream is None or not self.is_active:
            return None
            
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, self.stream.read, self.chunk_size)
            return data
        except Exception as e:
            logger.error(f"Error reading audio chunk: {e}")
            return None

    def get_rms(self, block):
        """Calculates RMS amplitude for visual meter."""
        shorts = np.frombuffer(block, dtype=np.int16)
        if len(shorts) == 0: return 0.0
        sum_squares = np.sum(shorts.astype(float)**2)
        return np.sqrt(sum_squares / len(shorts))
