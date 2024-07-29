import sublime
import sublime_plugin
from ..settings import PiecesSettings


class PiecesImportAssetCommand(sublime_plugin.WindowCommand):
	def run(self,sublime_snippets):
		dummy_view = self.window.create_output_panel("pieces_dummy_view",unlisted=True)
		dummy_view.run_command("insert_snippet", {"name": sublime_snippets})
		content = dummy_view.substr(sublime.Region(0, self.window.active_view().size()))
		self.window.views()[0].run_command("pieces_create_asset",{"data":content})
		
	def input(self,args):
		return SublimeSnippetsInputHandler()

	def is_enabled(self):
		return PiecesSettings.is_loaded

class SublimeSnippetsInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		snippets = sublime.find_resources("*.sublime-snippet")
		return [
			(snippet,snippet) for snippet in snippets
		]
	
