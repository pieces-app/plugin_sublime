from pieces_os_client import AssetsApi
from pieces.settings import PiecesSettings
from .list_assets import PiecesListAssetsCommand
import sublime
import sublime_plugin

class PiecesDeleteAssetCommand(sublime_plugin.WindowCommand):
	def run(self,asset_id=None):
		
		if not asset_id:
			sheet = self.window.active_sheet()
			sheet_details =  PiecesListAssetsCommand.sheets_md.get(sheet.id())
			if not sheet_details:
				return
			asset_id = sheet_details["id"]
			name = sheet_details["name"]
			msg = f"Are you sure you want to delete '{name}'"
		else:
			sheet = None
			msg = "Are you sure you want to delete this asset"
		

		if sublime.ok_cancel_dialog(msg,ok_title='Yes, I am sure',title="Warning"):
			delete_instance = AssetsApi(PiecesSettings.api_client)
			delete_instance.assets_delete_asset(asset_id)
			if sheet:
				sheet.close()
