import asyncio
import logging
from typing import Callable, Any, Dict, List

logger = logging.getLogger("Lucy-EventBus")

class EventBus:
    """
    Central Event Bus for modular communication.
    Modules can publish events and subscribe to them.
    """
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe a callback to an event type."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        logger.debug(f"Subscribed {callback.__name__ if hasattr(callback, '__name__') else 'callback'} to {event_type}")

    async def publish(self, event_type: str, data: Any = None):
        """Publish an event to all subscribers asynchronously."""
        if event_type not in self.subscribers:
            return

        logger.info(f"Event: {event_type} | Data: {str(data)[:100]}")
        
        # Call all subscribers in parallel
        tasks = []
        for callback in self.subscribers[event_type]:
            if asyncio.iscoroutinefunction(callback):
                tasks.append(callback(data))
            else:
                # Run synchronous callbacks in a thread pool
                loop = asyncio.get_running_loop()
                tasks.append(loop.run_in_executor(None, callback, data))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

# Singleton instance for global use
event_bus = EventBus()
