from pieces_os_client import QGPTStreamOutput

from ..settings import PiecesSettings
from ..base_websocket import BaseWebsocket

class AskStreamWS(BaseWebsocket):
	def __new__(cls,*args,**kwargs):
		if not hasattr(cls, 'instance'):
			cls.instance = super(AskStreamWS, cls).__new__(cls)
		return cls.instance

	@property
	def url(self):
		return PiecesSettings.ASK_STREAM_WS_URL

	def on_message(self,ws, message):
		self.on_message_callback(QGPTStreamOutput.from_json(message))

