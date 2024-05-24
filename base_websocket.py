import sublime
import sublime_plugin
import websocket
import threading

class BaseWebsocket:
	instances = []

	def __init__(self,on_message_callback=None):
		self.ws = None
		self.thread = None
		self.running = False
		self.on_message_callback = on_message_callback

		BaseWebsocket.instances.append(self)

	@property
	def url(self):
		return None

	def on_message(self, ws,message):
		pass

	def on_error(self, ws, error):
		print(f"Error: {error}")

	def on_close(self, ws, close_status_code, close_msg):
		pass

	def on_open(self,ws):
		self.running = True

	def run(self):
		self.ws = websocket.WebSocketApp(
			self.url,
			on_message=self.on_message,
			on_error=self.on_error,
			on_close=self.on_close
		)
		self.ws.on_open = self.on_open
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

	def close_all(cls):
		for instance in instances:
			instance.close()

	@classmethod
	def reconnect_all(cls):
		"""Reconnect all websocket instances."""
		for instance in cls.instances:
			instance.reconnect()

	def reconnect(self):
		"""Reconnect the websocket connection."""
		if not self.is_connected:
			self.start()

