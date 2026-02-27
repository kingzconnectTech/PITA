import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

# Server Configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8005

# Logging
LOG_LEVEL = "DEBUG"

# Voice Configuration
WAKE_WORD = "pita"
SAMP_RATE = 16000
CHANNELS = 1
INPUT_DEVICE_INDEX = 2 # Fixed for this environment

# STT Configuration (Faster Whisper)
WHISPER_MODEL = "tiny"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"

# TTS Configuration
TTS_ENGINE = "local" 

# LLM Configuration
LLM_PROVIDER = "ollama"
LLM_MODEL = "qwen2.5:7b"

# System Controller Config
ALLOWED_APPLICATIONS = ["code", "browser", "explorer", "terminal"]
SAFE_PATHS = [str(Path.home() / "Documents"), str(Path.home() / "Desktop")]

# VAD Configuration
VAD_AGGRESSIVENESS = 0 # Most sensitive
SILENCE_TIMEOUT = 1.0
MIN_SPEECH_DURATION = 0.3
