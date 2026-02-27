import json
import asyncio
import logging
import websockets
from pita.backend.config.settings import SERVER_HOST, SERVER_PORT
from pita.backend.core.event_bus import event_bus

logger = logging.getLogger("Lucy-API")

class WebSocketHandler:
    """
    Handles real-time communication with the frontend.
    Connects frontend events to the Lucy Core Event Bus.
    """
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.host = host
        self.port = port
        self.clients = set()
        
        # Subscribe to internal events to broadcast them to the frontend
        event_bus.subscribe("STATE_CHANGED", self.on_state_changed)
        event_bus.subscribe("MIC_LEVEL", self.on_mic_level)
        event_bus.subscribe("SYSTEM_RESPONSE", self.on_system_response)

    async def register(self, websocket):
        self.clients.add(websocket)
        logger.info(f"Client connected. Total: {len(self.clients)}")

    async def unregister(self, websocket):
        self.clients.remove(websocket)
        logger.info(f"Client disconnected. Total: {len(self.clients)}")

    async def handler(self, websocket):
        await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                # Forward frontend events to Lucy Core
                if "event" in data:
                    await event_bus.publish(f"FRONTEND_{data['event'].upper()}", data)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)

    async def broadcast(self, message_dict):
        if not self.clients: return
        message = json.dumps(message_dict)
        await asyncio.gather(*[client.send(message) for client in self.clients], return_exceptions=True)

    # Event Handlers for internal events
    async def on_state_changed(self, data):
        await self.broadcast({"state": data["new_state"], "text": data.get("reason", "")})

    async def on_mic_level(self, data):
        await self.broadcast({"type": "mic_level", "value": data["value"], "state": data["state"]})

    async def on_system_response(self, data):
        await self.broadcast({"state": "speaking", "text": data["text"]})

    async def run(self):
        logger.info(f"Starting WebSocket server on {self.host}:{self.port}...")
        try:
            async with websockets.serve(self.handler, self.host, self.port):
                await asyncio.Future() # Run forever
        except Exception as e:
            logger.error(f"WebSocket Server Failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise e
