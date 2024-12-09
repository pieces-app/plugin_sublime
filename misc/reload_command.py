from ..settings import PiecesSettings
from .._pieces_lib.pieces_os_client.wrapper.websockets import BaseWebsocket
import sublime
import sublime_plugin



class PiecesReloadCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		sublime.set_timeout_async(self.reload_async,0)

	
	def reload_async(self):
		if PiecesSettings.api_client.is_pieces_running():
			try:
				PiecesSettings.on_settings_change(all = True)
				sublime.status_message(f"Reloading [completed]")
			except Exception as e:
				sublime.error_message(f"Error during reload: {e}")
		else:
			sublime.status_message(f"PiecesOS is offline")

