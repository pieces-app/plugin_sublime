import asyncio
import websockets
from pieces.settings import PiecesSettings
import threading


class BaseWebsocket:
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

	async def close_websocket_connection(self):
		"""Close the websocket connection."""
		if self.ws and self.is_connected:
			await self.ws.close()
			self.is_connected = False

