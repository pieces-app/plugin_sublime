import sublime_plugin
from .ask_view import CopilotViewManager
from ..settings import PiecesSettings

copilot = CopilotViewManager()


class PiecesAskStreamCommand(sublime_plugin.WindowCommand):
	def run(self):
		copilot.ask_websocket.start()
		self.window.focus_view(copilot.gpt_view)
		return
	
	def is_enabled(self):
		return PiecesSettings().is_loaded


class PiecesEnterResponseCommand(sublime_plugin.TextCommand):
	def run(self,_):
		copilot.ask()

	def is_enabled(self):
		return PiecesSettings().is_loaded