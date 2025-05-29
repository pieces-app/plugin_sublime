import sublime_plugin
import sublime
from .ask_command import copilot,PiecesQueryInputHandler
from ..settings import PiecesSettings
from ..startup_utils import check_pieces_os


class PiecesAskStreamAboutCommand(sublime_plugin.TextCommand):
	@check_pieces_os()
	def run(self,edit,type,pieces_query=None):
		self.chat = PiecesSettings.api_client.copilot.create_chat()
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
			name = self.view.file_name()
			ext = ""
			if name:
				ext = name.split(".")[-1]
			self.before_query = f"\n```{ext}\n{data}\n```\n"

		if not pieces_query:
			sublime.active_window().show_input_panel("Enter a query", "", self.on_done, None, None)
			return

		self.on_done(pieces_query)

	def on_done(self,query):
		query = self.before_query + query
		copilot.render_conversation(self.chat.id)
		copilot.add_query(query) # Add the query
		copilot.gpt_view.run_command("pieces_enter_response")

	@check_pieces_os(True)
	def input(self, args):
		return PiecesQueryInputHandler()

