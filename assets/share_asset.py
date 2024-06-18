import sublime_plugin
from pieces_os_client import LinkifyApi,Linkify

from .utils import AssetSnapshot
from ..settings import PiecesSettings
from ..auth.auth_user import AuthUser


class PiecesGenerateShareableLinkCommand(sublime_plugin.WindowCommand):
	def run(self,asset_id):
		asset = AssetSnapshot.assets_snapshot[asset_id]
		user = AuthUser.user_profile
		if user:
			return LinkifyApi(PiecesSettings.api_client).linkify(async_req=True,
				linkify=Linkify(
					asset=asset,
					access="PUBLIC",
					)
				)


class PiecesShareAssetCommand(sublime_plugin.TextCommand):
	def run(self,edit,data):
		if not data:
			data = "\n".join([self.view.substr(selection) for selection in self.view.sel()])
