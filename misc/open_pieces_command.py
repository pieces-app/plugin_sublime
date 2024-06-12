import sublime_plugin
import sublime
from ..api import open_pieces_os

class PiecesOpenPiecesCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		sublime.set_timeout_async(self.run_async)

	@staticmethod
	def run_async():
		view = sublime.active_window().active_view()
		view.set_status("OPEN_STATUS","Opening Pieces OS") if view else None
		open_pieces_os()
		view.erase_status("OPEN_STATUS") if view else None
		sublime.status_message("Pieces OS lunched successfully")