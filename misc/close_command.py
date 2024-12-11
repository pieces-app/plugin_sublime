import sublime
import sublime_plugin
from ..settings import PiecesSettings
from .._pieces_lib.pieces_os_client.wrapper.websockets.health_ws import HealthWS


class PiecesCloseOsCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		PiecesSettings.api_client.os_api.os_terminate()
		sublime.status_message(f"PiecesOS closed successfully")
	
	def is_enabled(self):
		return HealthWS.instance.is_loaded
