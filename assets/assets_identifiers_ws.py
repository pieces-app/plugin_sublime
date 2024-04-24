import json
import asyncio
import pieces_os_client as pos_client
import websockets
from pieces import config 
import threading

class AssetsIdentifiersWS:
    def __init__(self, on_message_callback):
        self.ws = None
        self.is_connected = False
        self.on_message_callback = on_message_callback

        # Create a new event loop
        self.loop = asyncio.new_event_loop()

        # Run the event loop in a new thread
        self.thread = threading.Thread(target=self.start_event_loop, args=(self.loop,))
        self.thread.start()

        # Open the websocket connection
        asyncio.run_coroutine_threadsafe(self.open_websocket(), self.loop)

    def start_event_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def open_websocket(self):
        """Opens a websocket connection"""
        self.ws = await websockets.connect(config.ASSETS_IDENTIFIERS_WS_URL)
        self.is_connected = True
        try:
            async for message in self.ws:
                self.on_message_callback(json.loads(message))
        except websockets.exceptions.ConnectionClosed:
            self.is_connected = False
            

    # async def send_json(self, json):
    #     """Send a message over the websocket."""
    #     try:
    #         await self.ws.send(json)
    #     except websockets.exceptions.ConnectionClosed as e:
    #         print(f"Error sending message: {e}")
    #         self.is_connected = False
    #         await self.open_websocket()
    #         await self.send_json(json)

    async def close_websocket_connection(self):
        """Close the websocket connection."""
        if self.ws and self.is_connected:
            await self.ws.close()
            self.is_connected = False

