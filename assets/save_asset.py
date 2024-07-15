import sublime
import sublime_plugin
from .._pieces_lib.pieces_os_client import ClassificationGenericEnum,FormatApi
from ..settings import PiecesSettings
from .assets_snapshot import AssetSnapshot



class PiecesSaveAssetCommand(sublime_plugin.WindowCommand):
	def run(self,asset_id,data):
		AssetSnapshot(asset_id).edit_asset_original_format(data)

