import asyncio
import pieces_os_client as pos_client
import websockets
from pieces.settings import PiecesSettings
import threading

class AssetsIdentifiersWS:
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AssetsIdentifiersWS, cls).__new__(cls)
        return cls.instance
    def __init__(self, on_message_callback=None):
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
        if self.is_connected: # connect only once
            return
        self.ws = await websockets.connect(PiecesSettings.ASSETS_IDENTIFIERS_WS_URL)
        self.is_connected = True
        try:
            async for message in self.ws:
                self.on_message_callback(pos_client.StreamedIdentifiers.from_json(message))
        except websockets.exceptions.ConnectionClosed:
            self.is_connected = False
            

    async def close_websocket_connection(self):
        """Close the websocket connection."""
        if self.ws and self.is_connected:
            await self.ws.close()
            self.is_connected = False

