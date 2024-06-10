import sublime_plugin
from .ask_view import CopilotViewManager

copilot = CopilotViewManager()


class PiecesAskStreamCommand(sublime_plugin.WindowCommand):
	def run(self):
		copilot.ask_websocket.start()
		self.window.focus_view(copilot.gpt_view)
		return



class PiecesEnterResponseCommand(sublime_plugin.TextCommand):
	def run(self,_):
		copilot.ask()

