from pieces_os_client import StreamedIdentifiers
import websockets
import threading

from pieces.settings import PiecesSettings
from pieces.base_websocket import BaseWebsocket

class AssetsIdentifiersWS(BaseWebsocket):
	def __new__(cls,*args,**kwargs):
		if not hasattr(cls, 'instance'):
			cls.instance = super(AssetsIdentifiersWS, cls).__new__(cls)
		return cls.instance
	
	async def open_websocket(self):
		"""Opens a websocket connection"""
		if self.is_connected: # connect only once
			return
		self.ws = await websockets.connect(PiecesSettings.ASSETS_IDENTIFIERS_WS_URL)
		self.is_connected = True
		try:
			async for message in self.ws:
				threading.Thread(target = self.on_message_callback, args = (StreamedIdentifiers.from_json(message),)).start()
		except websockets.exceptions.ConnectionClosed:
			self.is_connected = False