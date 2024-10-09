from .base_websocket import BaseWebsocket

class HealthWS(BaseWebsocket):
	def __init__(self, pieces_client, 
		on_open_callback = None):
		self.is_loaded = False
		super().__init__(pieces_client, lambda x: None, on_open_callback, None,self.on_close)
	
	@property
	def url(self):
		return self.pieces_client.HEALTH_WS_URL

	def on_message(self, ws, message):

		if "ok" in message.lower():
			self.is_loaded = True
		else:
			self.is_loaded = False
			print("Please make sure Pieces OS is running")

	def on_close(self,ws,status_code,close_message):
		self.is_loaded = False