import sublime_plugin
import sublime
from pieces_os_client import LinkifyApi,Linkify

from .utils import AssetSnapshot
from .list_assets import PiecesListAssetsCommand
from ..settings import PiecesSettings
from ..auth.auth_user import AuthUser


class PiecesGenerateShareableLinkCommand(sublime_plugin.WindowCommand):
	def run(self,asset_id):
		self.asset_id = asset_id
		asset = AssetSnapshot.assets_snapshot[asset_id]
		user = AuthUser.user_profile
		if user:
			self.thread = LinkifyApi(PiecesSettings.api_client).linkify(async_req=True,
				linkify=Linkify(
					asset=asset,
					access="PUBLIC",
					)
				)
		sublime.set_timeout_async(self.run_async)

	def run_async(self):
		sheet = self.window.active_sheet()
		try:
			share = self.thread.get(120)
			if not sheet:
				return
			PiecesListAssetsCommand.shareable_link.remove(sheet.id())
			if sheet.id() in PiecesListAssetsCommand.sheets_md:
				PiecesListAssetsCommand.update_sheet(sheet,self.asset_id)
		except:	
			PiecesListAssetsCommand.shareable_link.remove(sheet.id())
			return
		


# class PiecesShareAssetCommand(sublime_plugin.TextCommand):
# 	def run(self,edit,data):
# 		if not data:
# 			data = "\n".join([self.view.substr(selection) for selection in self.view.sel()])
