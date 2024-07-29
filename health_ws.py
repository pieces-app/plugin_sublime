from .settings import PiecesSettings
from .base_websocket import BaseWebsocket

class HealthWS(BaseWebsocket):
	def __init__(self):
		super().__init__(lambda:None, [])

	@property
	def url(self):
		return PiecesSettings.HEALTH_WS_URL

	def on_message(self,ws, message):
		if message == "OK":
			PiecesSettings.is_loaded = True
		else:
			PiecesSettings.is_loaded = False

	def on_close(self, ws, close_status_code, close_msg):
		PiecesSettings.is_loaded = False # the websocket is closed
