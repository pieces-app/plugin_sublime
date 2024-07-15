from .._pieces_lib.pieces_os_client import AssetsApi
from ..settings import PiecesSettings
from .list_assets import PiecesListAssetsCommand
from .assets_snapshot import AssetSnapshot
import sublime
import sublime_plugin

class PiecesDeleteAssetCommand(sublime_plugin.WindowCommand):
	def run(self,asset_id=None):
		
		if not asset_id:
			sheet = self.window.active_sheet()
			asset_id =  PiecesListAssetsCommand.sheets_md.get(sheet.id())
			if not asset_id:
				return
			asset_wrapper = AssetSnapshot(asset_id)
			name = asset_wrapper.name
			msg = f"Are you sure you want to delete '{name}'"
		else:
			sheet = None
			msg = "Are you sure you want to delete this asset"
		

		if sublime.ok_cancel_dialog(msg,ok_title='Yes, I am sure',title="Warning"):
			delete_instance = AssetsApi(PiecesSettings.api_client)
			delete_instance.assets_delete_asset(asset_id)
			if sheet:
				sheet.close()
	def is_enabled(self):
		return PiecesSettings().is_loaded