import sublime_plugin
import mdpopups
from .assets.assets_snapshot import AssetSnapshot
from .assets.list_assets import PiecesAssetIdInputHandler
class PiecesShowCompletionDetailsCommand(sublime_plugin.TextCommand):
	def run(self,edit,asset_id):
		asset_wrapper = AssetSnapshot(asset_id)
		lang = asset_wrapper.original_classification_specific().value
		content = asset_wrapper.get_asset_raw()
		details = PiecesAssetIdInputHandler.get_annotation(asset_wrapper.asset)
		mdpopups.show_popup(
			self.view,
			f"{details.text if details else ''}\n```{lang}\n{content}\n```",max_width=900,
			wrapper_class="wrapper",
			css=".wrapper {margin:6px}")

