from ..settings import PiecesSettings
from .._pieces_lib.pieces_os_client.wrapper.websockets import BaseWebsocket
import sublime
import sublime_plugin



class PiecesReloadCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		sublime.set_timeout_async(self.reload_async,0)

	
	def reload_async(self):
		if PiecesSettings.api_client.health:
			try:
				sublime.set_timeout_async(self.run_reload_async)
			except Exception as e:
				sublime.error_message(f"Error during reload: {e}")
		else:
			sublime.status_message(f"Pieces OS is offline")

	@staticmethod
	def run_reload_async():
		PiecesSettings.on_settings_change(all = True)
		BaseWebsocket.reconnect_all()
		sublime.status_message(f"Reloading [completed]")

	def is_enabled(self) -> bool:
		return PiecesSettings.is_loaded