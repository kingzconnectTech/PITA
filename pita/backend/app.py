import asyncio
import logging
import time
import os
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))
from pita.backend.config.settings import LOG_LEVEL, SILENCE_TIMEOUT, WAKE_WORD, WAKE_WINDOW
from pita.backend.core.event_bus import event_bus
from pita.backend.core.state_manager import state_manager, LucyState

# New Architecture Modules
from pita.backend.audio.recorder import AudioRecorder
from pita.backend.audio.vad import VADEngine
from pita.backend.audio.stt import STTEngine
from pita.backend.intent.parser import IntentParser
from pita.backend.intent.planner import ActionPlanner
from pita.backend.executor.app_control import AppController
from pita.backend.executor.file_system import FileController
from pita.backend.executor.browser import BrowserController
from pita.backend.executor.system import SystemController
from pita.backend.memory.session import SessionMemory
from pita.backend.voice.tts import TTSEngine
from pita.backend.api.routes import WebSocketHandler
from pita.backend.voice.wake import WakeWordDetector
from pita.backend.intent.llm_provider import LLMProvider

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Lucy-Core")

class LucyAssistant:
    """
    Main entry point for Lucy Core.
    Coordinates all modules via the Event Bus.
    """
    def __init__(self):
        logger.info("Initializing Lucy Core...")
        
        # 1. Initialize Modules
        self.recorder = AudioRecorder()
        self.vad = VADEngine()
        self.stt = STTEngine()
        self.parser = IntentParser()
        self.planner = ActionPlanner()
        
        self.app_ctrl = AppController()
        self.file_ctrl = FileController()
        self.browser_ctrl = BrowserController()
        self.system_ctrl = SystemController()
        
        self.memory = SessionMemory()
        self.tts = TTSEngine()
        self.ws_handler = WebSocketHandler()
        self.wake = WakeWordDetector(WAKE_WORD)
        self.llm = LLMProvider()
        
        # 2. Subscribe to internal events
        event_bus.subscribe("SPEECH_CAPTURED", self.on_speech_captured)
        event_bus.subscribe("INTENT_READY", self.on_intent_ready)
        event_bus.subscribe("EXECUTION_REQUEST", self.on_execution_request)
        
        self.audio_buffer = []
        self.last_speech_time = 0
        self.wake_buffer = []
        self.wake_recording = False
        self.wake_last_time = 0

    async def run(self):
        """Starts the main Lucy Core event loop."""
        logger.info("Lucy Core is online.")
        
        try:
            # Start the WebSocket server
            asyncio.create_task(self.ws_handler.run())
            
            # Start the audio recorder
            self.recorder.start()
            
            while True:
                chunk = await self.recorder.read_chunk()
                if not chunk:
                    await asyncio.sleep(0.01)
                    continue

                # Get RMS for visual meter
                rms = self.recorder.get_rms(chunk)
                await event_bus.publish("MIC_LEVEL", {"value": float(rms), "state": state_manager.state.value})
                
                # VAD logic
                is_speech = self.vad.is_speech(chunk)
                current_time = time.time()
                
                if state_manager.state == LucyState.IDLE:
                    if is_speech:
                        if not self.wake_recording:
                            self.wake_recording = True
                            self.wake_buffer = []
                        self.wake_last_time = current_time
                        self.wake_buffer.append(chunk)
                    else:
                        if self.wake_recording:
                            silence = current_time - self.wake_last_time
                            if silence > WAKE_WINDOW:
                                text = await asyncio.to_thread(self.stt.transcribe, b"".join(self.wake_buffer))
                                self.wake_recording = False
                                self.wake_buffer = []
                                if self.wake.has_wake_word(text):
                                    await state_manager.transition_to(LucyState.LISTENING, "Wake word detected")
                                    self.audio_buffer = []
                
                if state_manager.state == LucyState.LISTENING:
                    self.audio_buffer.append(chunk)
                    
                    if not is_speech:
                        silence_duration = current_time - self.last_speech_time
                        if silence_duration > SILENCE_TIMEOUT:
                            await state_manager.transition_to(LucyState.PROCESSING, "Silence timeout")
                            # Publish speech captured event
                            full_audio = b"".join(self.audio_buffer)
                            self.audio_buffer = []
                            await event_bus.publish("SPEECH_CAPTURED", full_audio)
                
                await asyncio.sleep(0.01)
                
        except Exception as e:
            logger.error(f"Main loop error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise e
        finally:
            self.recorder.stop()

    # Event Handlers
    async def on_speech_captured(self, audio_data):
        """Step 1: Transcribe and parse intent."""
        text = await asyncio.to_thread(self.stt.transcribe, audio_data)
        if text:
            intent_data = await asyncio.to_thread(self.parser.parse, text)
            intent_data["raw_text"] = text
            await event_bus.publish("INTENT_READY", intent_data)
        else:
            await state_manager.transition_to(LucyState.IDLE, "No speech recognized")

    async def on_intent_ready(self, intent_data):
        """Step 2: Build execution plan."""
        plan = await asyncio.to_thread(self.planner.plan, intent_data)
        if plan:
            await event_bus.publish("EXECUTION_REQUEST", {"plan": plan, "raw_text": intent_data["raw_text"]})
        else:
            await state_manager.transition_to(LucyState.IDLE, "No plan generated")

    async def on_execution_request(self, data):
        """Step 3: Execute actions and give feedback."""
        await state_manager.transition_to(LucyState.EXECUTING, "Running plan")
        
        results = []
        for step in data["plan"]:
            action = step["action"]
            params = step["params"]
            
            # Simple routing to executors
            if action == "open_folder":
                res = self.file_ctrl.open_folder(params["target"])
            elif action == "browser_search":
                res = self.browser_ctrl.search(params["target"])
            elif action == "type_text":
                res = self.system_ctrl.type_text(params["target"])
            else:
                res = f"Unknown action: {action}"
            results.append(res)

        final_result = " ".join(results)
        self.memory.add_interaction(data["raw_text"], final_result)
        
        # Final feedback
        await state_manager.transition_to(LucyState.SPEAKING, "Giving feedback")
        assistant_text = data.get("raw_text", "")
        try:
            sys_prompt = "You are Lucy, a helpful local assistant. Summarize actions briefly and respond conversationally."
            prompt = f"User: {data.get('raw_text','')}\nActions result: {final_result}\nRespond:"
            assistant_text = await asyncio.to_thread(self.llm.generate, prompt, sys_prompt)
        except Exception as e:
            assistant_text = final_result
        await event_bus.publish("SYSTEM_RESPONSE", {"text": assistant_text})
        await asyncio.to_thread(self.tts.speak, assistant_text)
        
        await asyncio.sleep(1.0) # Let user see/hear
        await state_manager.transition_to(LucyState.IDLE, "Ready")

if __name__ == "__main__":
    import sys
    try:
        print("STARTING LUCY CORE...", flush=True)
        lucy = LucyAssistant()
        print("LUCY CORE READY.", flush=True)
        asyncio.run(lucy.run())
    except Exception as e:
        print(f"LUCY CORE CRASHED: {e}", flush=True)
        import traceback
        traceback.print_exc()
