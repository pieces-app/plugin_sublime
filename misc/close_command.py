import sublime
import sublime_plugin
from ..settings import PiecesSettings



class PiecesCloseOsCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		PiecesSettings.api_client.os_api.os_terminate()
		sublime.status_message(f"Pieces OS closed successfully")
	
	def is_enabled(self):
		return PiecesSettings.is_loaded
