import sublime_plugin
import sublime
from .ask_command import copilot
from ..assets.create_asset import PiecesCreateAssetCommand

class PiecesAskStreamAboutCommand(sublime_plugin.TextCommand):
	def run(self,edit,type):
		self.before_query = ""
		if type == "file":
			path = self.view.file_name()
			if not path: return 

			placeholder = "Ask about that file"
			self.context = {"paths":[path]}
		elif type == "folder":
			window = self.view.window()
			if not window: return
			paths = window.folders()
			if not paths: return

			self.context = {"paths":paths}
			placeholder = "Ask a question about your current project"

		elif type == "section":
			seed = PiecesCreateAssetCommand(self.view).get_seeds()
			if not seed: return
			self.before_query = str(seed.asset.format.fragment.string.raw)
			self.context = {"seed":seed}
			placeholder = "Ask about the current section"

		self.view.window().show_input_panel(placeholder, "",self.on_done, None, None)
		
	def on_done(self,query):
		copilot.render_conversation(None) # Create conversation if not already
		copilot.add_context(**self.context)
		if self.before_query: query = self.before_query + query
		copilot.add_query(query) # Add the query


