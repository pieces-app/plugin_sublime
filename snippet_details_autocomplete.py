from ._pieces_lib.pieces_os_client.wrapper.basic_identifier.asset import BasicAsset
import sublime_plugin
import mdpopups

class PiecesShowCompletionDetailsCommand(sublime_plugin.TextCommand):
	def run(self,edit,asset_id):
		asset_wrapper = BasicAsset(asset_id)
		lang = asset_wrapper.classification.value if asset_wrapper.classification else "txt"
		content = asset_wrapper.raw_content
		details = asset_wrapper.description
		mdpopups.show_popup(
			self.view,
			f"{details.text if details else ''}\n```{lang}\n{content}\n```",max_width=900,
			wrapper_class="wrapper",
			css=".wrapper {margin:6px}")

