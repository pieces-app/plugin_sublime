from Pieces._pieces_lib.pieces_os_client.models.model_download_progress import ModelDownloadProgress
from Pieces._pieces_lib.pieces_os_client.wrapper.websockets.base_websocket import BaseWebsocket

from typing import TYPE_CHECKING, Callable, Optional
if TYPE_CHECKING:
	import Pieces._pieces_lib.websocket as websocket
	from Pieces._pieces_lib.pieces_os_client.wrapper import PiecesClient


class ModelDownloadWS(BaseWebsocket):
	def __init__(self, pieces_client: "PiecesClient", model_id, on_message_callback: Callable[[ModelDownloadProgress], None], on_open_callback: Optional[Callable[["websocket.WebSocketApp"], None]] = None, on_error: Optional[Callable[["websocket.WebSocketApp", Exception], None]] = None, on_close: Optional[Callable[["websocket.WebSocketApp", str, str], None]] = None):
		self.model_id = model_id
		ws_base_url:str = pieces_client.host.replace('http','ws')
		self._url = ws_base_url + f"/model/{model_id}/download/progress"
		super().__init__(pieces_client, on_message_callback, on_open_callback, on_error, on_close)
	
	@property
	def url(self):
		return self._url

	def on_message(self, ws, message):
		self.on_message_callback(ModelDownloadProgress.from_json(message))

