import sublime_plugin
import sublime
from ..settings import PiecesSettings

class PiecesOpenPiecesCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		sublime.set_timeout_async(self.run_async)

	@staticmethod
	def run_async(show_dialog: bool = True) -> bool:
		if PiecesSettings.api_client.is_pieces_running():
			sublime.status_message("PiecesOS is already running")
			return False
		view = sublime.active_window().active_view()
		view.set_status("OPEN_STATUS","Opening PiecesOS") if view else None
		if PiecesSettings.api_client.open_pieces_os():
			view.erase_status("OPEN_STATUS") if view else None
			sublime.status_message("PiecesOS launched successfully")
			sublime.run_command("pieces_reload")
			return True
		else:
			view.erase_status("OPEN_STATUS") if view else None
			sublime.status_message("Unable to launch PiecesOS")
			if show_dialog and sublime.ok_cancel_dialog("PiecesOS could not be launched. Would you like to install it?"):
				sublime.active_window().run_command("pieces_install_pieces_os")
			return False