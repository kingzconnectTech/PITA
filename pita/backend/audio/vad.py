import logging
import numpy as np
from pita.backend.config.settings import VAD_AGGRESSIVENESS

logger = logging.getLogger("Lucy-VAD")

class VADEngine:
    """
    Simple Energy-based Voice Activity Detection.
    Doesn't require ML dependencies.
    """
    def __init__(self):
        # Scale aggressiveness: 0 (most sensitive) to 3 (least sensitive)
        # Threshold for RMS energy
        self.threshold = 100 + (VAD_AGGRESSIVENESS * 150)
        logger.info(f"Energy-based VAD initialized. Threshold: {self.threshold}")

    def is_speech(self, audio_chunk):
        try:
            audio_int16 = np.frombuffer(audio_chunk, dtype=np.int16)
            if len(audio_int16) == 0:
                return False
                
            # Calculate RMS energy
            rms = np.sqrt(np.mean(audio_int16.astype(float)**2))
            
            # For debugging, log occasionally if there's any sound
            if rms > 50:
                logger.debug(f"VAD RMS: {rms:.2f} (Threshold: {self.threshold})")
            
            return rms > self.threshold
        except Exception as e:
            logger.error(f"VAD Error: {e}")
            return False
