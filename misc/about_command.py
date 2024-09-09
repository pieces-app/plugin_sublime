from ..settings import PiecesSettings
import sublime
import sublime_plugin
import mdpopups
from .. import __version__


md_text = f"""
# Pieces
## Discover
- [Plugins](https://code.pieces.app/plugins)

## Community
- [Become a beta tester](https://getpieces.typeform.com/to/XGGlUqEI?os=8c0a0a63-6fc6-43e3-a2c4-7690aefde52d)
- [Pieces Blogs](https://code.pieces.app/blog)

## Support
- <a href="subl:pieces_support">Get Support</a>
- [Submit your feedback](https://getpieces.typeform.com/to/mCjBSIjF?os=8c0a0a63-6fc6-43e3-a2c4-7690aefde52d){{notes}}

## Social Media
- [Website](https://pieces.app/)
- [Twitter](https://twitter.com/getpieces)
- [YouTube](https://www.youtube.com/@getpieces)
- [Discord](https://discord.gg/getpieces)
- [Reddit](https://www.reddit.com/r/PiecesForDevelopers/)

## Version
- Plugin Version: {__version__}
- Pieces Version: {PiecesSettings.api_client.version if PiecesSettings.api_client.is_pieces_running() else "Unknown"}
"""
class PiecesAboutCommand(sublime_plugin.WindowCommand):
	def run(self):
		version = "install" if __version__ == "1.0.0" else __version__
		resources = sublime.find_resources("*.txt")
		notes = [resource for resource in resources if resource.endswith(f"Pieces/messages/{version}.txt")]
		if notes:
			notes = f"""\n- <a href='subl:pieces_open_notes {{"path":"{notes[0]}"}}'>Release Notes</a>"""
		else:
			notes = ""

		mdpopups.new_html_sheet(self.window,"About Pieces For Developers",md_text.format(notes=notes),wrapper_class="wrapper",css=".wrapper {margin-left:4px}")

class PiecesOpenNotesCommand(sublime_plugin.WindowCommand):
	def run(self,path):
		text = sublime.load_resource(path).replace("\r","")
		file = self.window.new_file()
		file.set_name(path.split("/")[-1])
		file.run_command("append",{"characters":text})
		file.set_read_only(True)
		file.set_scratch(True)

