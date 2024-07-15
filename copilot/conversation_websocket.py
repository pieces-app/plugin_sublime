from .._pieces_lib.pieces_os_client import StreamedIdentifiers

from ..settings import PiecesSettings
from ..base_websocket import BaseWebsocket

class ConversationWS(BaseWebsocket):
	@property
	def url(self):
		return PiecesSettings.CONVERSATION_WS_URL

	def on_message(self,ws, message):
		self.on_message_callback(StreamedIdentifiers.from_json(message))
