import asyncio
import websockets
from .settings import PiecesSettings
import threading


class BaseWebsocket:
	instances = []

	def __init__(self, on_message_callback=None):
		self.ws = None
		self.is_connected = False
		self.on_message_callback = on_message_callback

		# Create a new event loop
		self.loop = asyncio.new_event_loop()

		# Run the event loop in a new thread
		self.thread = threading.Thread(target=self.loop.run_forever)
		self.thread.start()

		# Open the websocket connection
		asyncio.run_coroutine_threadsafe(self.open_websocket(), self.loop)


		# Add instance to the class-level list
		BaseWebsocket.instances.append(self)

	async def open_websocket(self):
		"""Open the websocket connection."""
		pass

	async def close_websocket_connection(self):
		"""Close the websocket connection."""
		if self.ws and self.is_connected:
			await self.ws.close()
			self.is_connected = False

	@classmethod
	def reconnect_all(cls):
		"""Reconnect all websocket instances."""
		for instance in cls.instances:
			asyncio.run_coroutine_threadsafe(instance.reconnect(), instance.loop)

	async def reconnect(self):
		"""Reconnect the websocket connection."""
		if not self.is_connected:
			await self.open_websocket()

