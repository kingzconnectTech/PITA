import logging
from enum import Enum
from pita.backend.core.event_bus import event_bus

logger = logging.getLogger("Lucy-StateManager")

class LucyState(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    EXECUTING = "executing"
    SPEAKING = "speaking"
    ERROR = "error"

class StateManager:
    """
    Manages Lucy's current operational state.
    Prevents conflicting states and notifies via Event Bus.
    """
    def __init__(self):
        self._current_state = LucyState.IDLE
        logger.info(f"State Manager initialized. Current State: {self._current_state.value}")

    @property
    def state(self) -> LucyState:
        return self._current_state

    async def transition_to(self, new_state: LucyState, reason: str = None):
        """Safely transition to a new state."""
        if new_state == self._current_state:
            return

        old_state = self._current_state
        self._current_state = new_state
        
        logger.info(f"State Transition: {old_state.value} -> {new_state.value} (Reason: {reason})")
        
        # Publish state change event
        await event_bus.publish("STATE_CHANGED", {
            "old_state": old_state.value,
            "new_state": new_state.value,
            "reason": reason
        })

# Singleton instance
state_manager = StateManager()
