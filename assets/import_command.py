import sublime
import sublime_plugin
import xml.etree.ElementTree as ET

class PiecesImportAssetCommand(sublime_plugin.WindowCommand):
	def run(self,sublime_snippets):
		content = sublime.load_resource(sublime_snippets)
		tree = ET.fromstring(content)
		content = tree.find('content').text
		self.window.views()[0].run_command("pieces_create_asset",{"data":content})
		
	def input(self,args):
		return SublimeSnippetsInputHandler()

class SublimeSnippetsInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		snippets = sublime.find_resources("*.sublime-snippet")
		return [
			(snippet,snippet) for snippet in snippets
		]
