import sys
from pathlib import Path
root = Path(__file__).resolve().parent
sys.path.append(str(root))

print("Testing all imports...")
try:
    import asyncio
    import logging
    import time
    from pita.backend.config.settings import LOG_LEVEL, SILENCE_TIMEOUT
    print("Core imports OK")
    from pita.backend.core.event_bus import event_bus
    print("Event bus OK")
    from pita.backend.core.state_manager import state_manager, LucyState
    print("State manager OK")
    from pita.backend.audio.recorder import AudioRecorder
    print("Recorder OK")
    from pita.backend.audio.vad import VADEngine
    print("VAD OK")
    from pita.backend.audio.stt import STTEngine
    print("STT OK")
    from pita.backend.intent.parser import IntentParser
    print("Parser OK")
    from pita.backend.intent.planner import ActionPlanner
    print("Planner OK")
    from pita.backend.executor.app_control import AppController
    print("AppControl OK")
    from pita.backend.executor.file_system import FileController
    print("FileSystem OK")
    from pita.backend.executor.browser import BrowserController
    print("Browser OK")
    from pita.backend.executor.system import SystemController
    print("System OK")
    from pita.backend.memory.session import SessionMemory
    print("Memory OK")
    from pita.backend.voice.tts import TTSEngine
    print("TTS OK")
    from pita.backend.api.routes import WebSocketHandler
    print("API OK")
    print("ALL IMPORTS SUCCESSFUL")
except Exception as e:
    print(f"IMPORT FAILED: {e}")
    import traceback
    traceback.print_exc()
