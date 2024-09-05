import sublime
import sublime_plugin
from .._pieces_lib.pieces_os_client import ClassificationGenericEnum,FormatApi
from .._pieces_lib.pieces_os_client.wrapper.basic_identifier.asset import BasicAsset
from ..settings import PiecesSettings
from .assets_snapshot import AssetSnapshot



class PiecesSaveAssetCommand(sublime_plugin.WindowCommand):
	def run(self,asset_id,data):
		BasicAsset(asset_id).raw_content = data

