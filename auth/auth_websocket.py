from ..base_websocket import BaseWebsocket
from ..settings import PiecesSettings
from pieces_os_client import UserProfile

import websockets

class AuthWebsocket(BaseWebsocket):

	def __new__(cls,*args,**kwargs):
		if not hasattr(cls, 'instance'):
			cls.instance = super(AuthWebsocket, cls).__new__(cls)
		return cls.instance

	async def open_websocket(self):
		"""Opens a websocket connection"""
		if self.is_connected: # connect only once
			return
		self.ws = await websockets.connect(PiecesSettings.AUTH_WS_URL)
		self.is_connected = True
		try:
			async for message in self.ws:
				if message == "":
					self.on_message_callback()
				else:
					self.on_message_callback(UserProfile.from_json(message))
		except websockets.exceptions.ConnectionClosed:
			self.is_connected = False