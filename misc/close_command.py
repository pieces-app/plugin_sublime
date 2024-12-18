import sublime
import sublime_plugin
from ..settings import PiecesSettings


class PiecesCloseOsCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		PiecesSettings.api_client.os_api.os_terminate()
		sublime.status_message(f"PiecesOS closed successfully")
	
	def is_enabled(self):
		return PiecesSettings.api_client.is_pos_stream_running