from ..base_websocket import BaseWebsocket
from ..settings import PiecesSettings
from pieces_os_client import UserProfile
import threading
import json


class AuthWebsocket(BaseWebsocket):
	def __new__(cls,*args,**kwargs):
		if not hasattr(cls, 'instance'):
			cls.instance = super(AuthWebsocket, cls).__new__(cls)
		return cls.instance

	@property
	def url(self):
		return PiecesSettings.AUTH_WS_URL

	def on_message(self,ws, message):
		try:
			self.on_message_callback(UserProfile.from_json(message))
		except json.decoder.JSONDecodeError:
			self.on_message_callback(None) # User logged out!

