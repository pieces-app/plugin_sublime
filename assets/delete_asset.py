from .._pieces_lib.pieces_os_client.wrapper.basic_identifier import BasicAsset
from ..startup_utils import check_pieces_os
from .list_assets import PiecesListAssetsCommand
import sublime
import sublime_plugin

class PiecesDeleteAssetCommand(sublime_plugin.WindowCommand):
	@check_pieces_os()
	def run(self,asset_id=None):
		if not asset_id:
			sheet = self.window.active_sheet()
			asset_id =  PiecesListAssetsCommand.sheets_md.get(sheet.id())
			if not asset_id:
				return
			asset_wrapper = BasicAsset(asset_id)
			name = asset_wrapper.name
			msg = f"Are you sure you want to delete '{name}'"
		else:
			sheet = None
			asset_wrapper = BasicAsset(asset_id)
			msg = f"Are you sure you want to delete '{asset_wrapper.name}'"
		

		if sublime.ok_cancel_dialog(msg,ok_title='Yes, I am sure',title="Warning"):
			asset_wrapper.delete()
			if sheet:
				sheet.close()

