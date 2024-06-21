import sublime
import sublime_plugin
from .._pieces_lib.pieces_os_client import ClassificationGenericEnum,FormatApi
from .utils import AssetSnapshot
from ..settings import PiecesSettings



class PiecesSaveAssetCommand(sublime_plugin.WindowCommand):
	def run(self,asset_id,data):
		asset = AssetSnapshot.assets_snapshot[asset_id]
		format_api = FormatApi(PiecesSettings.api_client)
		original = format_api.format_snapshot(asset.original.id, transferable=True)
		if original.classification.generic == ClassificationGenericEnum.IMAGE:
			sublime.error_message("Could not edit an image")
			return

		if original.fragment.string.raw:
			original.fragment.string.raw = data
		elif original.file.string.raw:
			original.file.string.raw = data
		format_api.format_update_value(transferable=False, format=original)

