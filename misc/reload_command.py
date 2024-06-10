from ..settings import PiecesSettings
from ..base_websocket import BaseWebsocket
import sublime
import sublime_plugin



class PiecesReloadCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		sublime.set_timeout_async(self.reload_async,0)

	@staticmethod
	def reload_async():
		if PiecesSettings.get_health():
			try:
				PiecesSettings.on_settings_change(all = True)
				BaseWebsocket.reconnect_all()
				PiecesSettings.is_loaded = True
				sublime.status_message(f"Reloading [completed]")
			except Exception as e:
				sublime.error_message(f"Error during reload: {e}")
		else:
			sublime.status_message(f"Pieces OS is offline")

