from pieces_os_client import StreamedIdentifiers,StreamedIdentifier,ReferencedAsset,AssetsApi
import threading
import sublime

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
		sublime.windows

	def on_error(self,ws,error): # Some issues with the dns so we need to warn the user the websocket is not running
		if type(error) == OSError:
			iterable = AssetsApi(PiecesSettings.api_client).assets_identifiers_snapshot().iterable
			streamed_idetifiers = StreamedIdentifiers(
				iterable = [
					StreamedIdentifier(asset = ReferencedAsset(id = asset.id)) for asset in iterable
				]
			)
			self.on_message_callback(streamed_idetifiers)
			sublime.message_dialog(
				"Warning: The Pieces package is unable to connect to the websocket.\n"
				"As a result, assets and certain functionalities will not be updated in real-time."
			)
		print(error)