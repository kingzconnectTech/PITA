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
            
        try:
            self.stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.rate,
                input=True,
                input_device_index=self.device_index,
                frames_per_buffer=self.chunk_size
            )
            self.is_active = True
            logger.info(f"Microphone stream started (Device Index: {self.device_index if self.device_index is not None else 'Default'}).")
        except Exception as e:
            logger.error(f"Failed to start microphone stream: {e}")
            raise e

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
