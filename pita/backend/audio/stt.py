import logging
import numpy as np
import speech_recognition as sr
import io
import wave

logger = logging.getLogger("Lucy-STT")

class STTEngine:
    """
    Speech-To-Text Layer using SpeechRecognition (Google fallback).
    Doesn't require ML heavy dependencies.
    """
    def __init__(self):
        self.recognizer = sr.Recognizer()
        logger.info("SpeechRecognition STT initialized.")

    def transcribe(self, audio_data):
        logger.info("Transcribing...")
        try:
            # Convert raw bytes to AudioData
            # We need to wrap it in a WAV container for SpeechRecognition
            buffer = io.BytesIO()
            with wave.open(buffer, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2) # 16-bit
                wav_file.setframerate(16000)
                wav_file.writeframes(audio_data)
            
            buffer.seek(0)
            with sr.AudioFile(buffer) as source:
                audio = self.recognizer.record(source)
            
            # Using Google Web Speech API (requires internet)
            # If no internet, we might need a local fallback like pocket-sphinx
            text = self.recognizer.recognize_google(audio)
            
            logger.info(f"Transcribed: '{text}'")
            return text
        except sr.UnknownValueError:
            logger.info("SpeechRecognition could not understand audio.")
            return ""
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service; {e}")
            return ""
        except Exception as e:
            logger.error(f"STT Error: {e}")
            return ""
