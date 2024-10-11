import sublime
import sublime_plugin
import xml.etree.ElementTree as ET
from .create_asset import PiecesCreateAssetCommand
from .ext_map import file_map

from ..startup_utils import check_pieces_os
from ..progress_bar import ProgressBar
from .._pieces_lib.pieces_os_client import FragmentMetadata



class PiecesImportAssetCommand(sublime_plugin.WindowCommand):
	@check_pieces_os()
	def run(self,sublime_snippets):
		def save(snippet, open_on_save, run_async = True):
			dummy_view = self.window.create_output_panel("pieces_dummy_view",unlisted=True)
			dummy_view.run_command("insert_snippet", {"name": snippet})
			content = dummy_view.substr(sublime.Region(0, dummy_view.size()))
			snippet_xml = sublime.load_resource(snippet)
			tree = ET.fromstring(snippet_xml)
			scope = tree.find('scope')
			metadata = None
			if scope:
				ext = file_map.reverse.get(sublime.find_syntax_by_name(scope.text))
				metadata = FragmentMetadata(ext = ext) if ext else None

			PiecesCreateAssetCommand(
				dummy_view
			).run(
				"",
				content,
				add_metadata=False, # automatically extracting the metadata should be false
				metadata = metadata,
				open_on_save=open_on_save,
				run_async = run_async,
				tags = ["Sublime", "Sublime Snippet", ".sublime_snippet"]
			)

		if sublime_snippets == "all":
			snippets = sublime.find_resources("*.sublime-snippet")

			def run_async():
				view = self.window.active_view()
				snippets_len = len(snippets)
				progress_bar = ProgressBar("Pieces Importing Snippets:",total=snippets_len)
				progress_bar.start()
				for idx,snippet in enumerate(snippets,start=1):
					save(snippet, open_on_save = False, run_async=False)
					progress_bar.update_progress(idx)
				progress_bar.stop()

				view.erase_status("import_snippet") if view else None

			sublime.set_timeout_async(run_async)
		else:
			save(sublime_snippets, open_on_save = True)
		
	@check_pieces_os(True)
	def input(self,args):
		return SublimeSnippetsInputHandler()



class SublimeSnippetsInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		snippets = sublime.find_resources("*.sublime-snippet")
		return [
			(f"Import All ({len(snippets)} Snippets)", "all"),
			*[(snippet,snippet) for snippet in snippets]
		]
	
