import sublime_plugin
import sublime
from ..settings import PiecesSettings

class PiecesOpenPiecesCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		sublime.set_timeout_async(self.run_async)

	@staticmethod
	def run_async():
		if PiecesSettings.api_client.is_pieces_running():
			return sublime.status_message("Pieces OS is already running")
		view = sublime.active_window().active_view()
		view.set_status("OPEN_STATUS","Opening Pieces OS") if view else None
		if PiecesSettings.api_client.open_pieces_os():
			view.erase_status("OPEN_STATUS") if view else None
			sublime.run_command("pieces_reload")
			sublime.status_message("Pieces OS lunched successfully")
		else: 
			view.erase_status("OPEN_STATUS") if view else None
			sublime.status_message("Unable to lunch Pieces OS")