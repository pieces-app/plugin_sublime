from typing import Optional
from ._pieces_lib.typing_extensions import Self
from ._pieces_lib import websocket
import threading
from abc import ABC, abstractmethod

class BaseWebsocket(ABC):
	instances = []
	def __new__(cls,*args,**kwargs):
		if not hasattr(cls, 'instance'):
			cls.instance = super(BaseWebsocket, cls).__new__(cls)
		return cls.instance

	def __init__(self, on_message_callback,on_open_callbacks=[]):
		self.ws = None
		self.thread = None
		self.running = False
		self.on_message_callback = on_message_callback
		self.on_open_callbacks = on_open_callbacks

		if self not in BaseWebsocket.instances:
			BaseWebsocket.instances.append(self)

	@abstractmethod
	def url(self) -> str:
		"""The URL to connect to. Should be overridden."""
		pass


	@abstractmethod
	def on_message(self, ws, message):
		pass

	def on_error(self, ws, error):
		print(f"Error: {error}")

	def on_close(self, ws, close_status_code, close_msg):
		pass

	def on_open(self, ws):
		self.running = True
		for callback in self.on_open_callbacks:
			callback()

	def run(self):
		self.ws = websocket.WebSocketApp(
			self.url,
			on_message=self.on_message,
			on_error=self.on_error,
			on_close=self.on_close,
			on_open=self.on_open
		)
		self.ws.run_forever()

	def start(self):
		if not self.running:
			self.thread = threading.Thread(target=self.run)
			self.thread.start()

	def close(self):
		if self.running:
			self.ws.close()
			self.thread.join()
			self.running = False

	@classmethod
	def close_all(cls):
		for instance in cls.instances:
			instance.close()

	@classmethod
	def reconnect_all(cls):
		"""Reconnect all websocket instances."""
		for instance in cls.instances:
			instance.reconnect()

	def reconnect(self):
		"""Reconnect the websocket connection."""
		self.close()
		self.start()

	def __str__(self):
		return getattr(self, "url", self.instances)

	@classmethod
	def is_running(cls) -> bool:
		instance = cls.get_instance()
		if instance:
			return cls.instance.running
		return False

	@classmethod
	def get_instance(cls) -> Optional[Self]:
		return getattr(cls,'instance',None)