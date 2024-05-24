from pieces_os_client import StreamedIdentifiers
import threading

from ..settings import PiecesSettings
from ..base_websocket import BaseWebsocket

class AssetsIdentifiersWS(BaseWebsocket):
	def __new__(cls,*args,**kwargs):
		if not hasattr(cls, 'instance'):
			cls.instance = super(AssetsIdentifiersWS, cls).__new__(cls)
		return cls.instance

	@property
	def url(self):
		return PiecesSettings.ASSETS_IDENTIFIERS_WS_URL

	def on_message(self,ws, message):
		self.on_message_callback(StreamedIdentifiers.from_json(message))

