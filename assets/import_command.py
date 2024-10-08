import sublime
import sublime_plugin
from ..settings import PiecesSettings
from .create_asset import PiecesCreateAssetCommand

class PiecesImportAssetCommand(sublime_plugin.WindowCommand):
	def run(self,sublime_snippets):
		def save(snippet, open_on_save):
			dummy_view = self.window.create_output_panel("pieces_dummy_view",unlisted=True)
			dummy_view.run_command("insert_snippet", {"name": snippet})
			content = dummy_view.substr(sublime.Region(0, dummy_view.size()))
			PiecesCreateAssetCommand(
				dummy_view
			).run(
				"",
				content,
				add_metadata=False,
				open_on_save=open_on_save,
				tags = ["Sublime", "Sublime Snippet", ".sublime_snippet"]
			)

		if sublime_snippets == "all":
			snippets = sublime.find_resources("*.sublime-snippet")

			def run_async():
				view = self.window.active_view()
				snippets_len = len(snippets)
				for idx,snippet in enumerate(snippets,start=1):
					if view:
						view.set_status("import_snippet", f"Pieces Importing Snippets: {idx}/{snippets_len}")
					save(snippet, open_on_save = False)

				view.erase_status("import_snippet") if view else None

			sublime.set_timeout_async(run_async)
		else:
			save(sublime_snippets, open_on_save = True)
		
		
	def input(self,args):
		return SublimeSnippetsInputHandler()

	def is_enabled(self):
		return PiecesSettings.is_loaded

class SublimeSnippetsInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		snippets = sublime.find_resources("*.sublime-snippet")
		return [
			("Import All", "all"),
			(snippet,snippet) for snippet in snippets
		]
	
