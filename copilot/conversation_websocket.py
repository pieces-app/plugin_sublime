from pieces_os_client import StreamedIdentifiers

from ..settings import PiecesSettings
from ..base_websocket import BaseWebsocket

class ConversationWS(BaseWebsocket):
	def __new__(cls,*args,**kwargs):
		if not hasattr(cls, 'instance'):
			cls.instance = super(ConversationWS, cls).__new__(cls)
		return cls.instance

	@property
	def url(self):
		return PiecesSettings.CONVERSATION_WS_URL

	def on_message(self,ws, message):
		self.on_message_callback(StreamedIdentifiers.from_json(message))
