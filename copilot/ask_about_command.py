import sublime_plugin
import sublime
from .ask_command import copilot,PiecesQueryInputHandler
from ..settings import PiecesSettings


class PiecesAskStreamAboutCommand(sublime_plugin.TextCommand):
	def run(self,edit,type,pieces_query=None):
		self.before_query = ""
		if type == "file":
			path = self.view.file_name()
			if not path: return 
			PiecesSettings.api_client.copilot.context.paths.append(path)

		elif type == "folder":
			window = self.view.window()
			if not window: return
			paths = window.folders()
			if not paths: return
			[PiecesSettings.api_client.copilot.context.paths.append(path) for path in paths]

		elif type == "section":
			# Get the all the selected text
			data = "\n".join([self.view.substr(selection) for selection in self.view.sel()])
			if not data:
				return sublime.error_message("Please select a text")
			PiecesSettings.api_client.copilot.context.raw_assets.append(data)

		if not pieces_query:
			sublime.active_window().show_input_panel("Enter a query", "", self.on_done, None, None)
			return

		if self.before_query: 
			pieces_query = self.before_query + pieces_query
		self.on_done(pieces_query)

	def on_done(self,query):
		copilot.render_conversation(None)
		copilot.add_query(query) # Add the query
		copilot.gpt_view.run_command("pieces_enter_response")

	def is_enabled(self):
		return PiecesSettings.is_loaded

	def input(self, args):
		return PiecesQueryInputHandler()

