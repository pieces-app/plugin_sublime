from .._pieces_lib.pieces_os_client import QGPTStreamOutput,QGPTStreamInput
from .._pieces_lib.websocket import WebSocketConnectionClosedException

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

	
	def send_message(self,message:QGPTStreamInput):
		try:
			if not self.ws:
				raise WebSocketConnectionClosedException()
			self.ws.send(message.to_json())
		except WebSocketConnectionClosedException:
			self.start() # Start a new websocket since we are not connected to any
			self.on_open = lambda ws: ws.send(message.to_json()) # Send the message on opening