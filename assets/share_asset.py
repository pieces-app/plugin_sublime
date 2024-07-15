import sublime_plugin
import sublime
from .._pieces_lib.pieces_os_client import LinkifyApi,Linkify

from .assets_snapshot import AssetSnapshot
from .list_assets import PiecesListAssetsCommand
from .create_asset import PiecesCreateAssetCommand
from ..settings import PiecesSettings
from ..auth.auth_user import AuthUser


class PiecesShareAssetCommand(sublime_plugin.WindowCommand):
	def run(self,asset_id,update_sheet=False):
		self.update_sheet = update_sheet
		self.sheet = self.window.active_sheet()
		if update_sheet:
			PiecesListAssetsCommand.update_sheet(self.sheet,asset_id,{"share":{"title":"Sharing","url":"noop"}})
		sublime.set_timeout_async(lambda:self.run_async(asset_id))

	def run_async(self,asset_id=None,seed=None):
		"""
			You need to either give the seed or the asset_id
		"""
		if asset_id:
			kwargs = {"asset" : AssetSnapshot.get_asset(asset_id)}
		else:
			kwargs = {"seed" : seed}
		user = AuthUser.user_profile
		if not user:
			if sublime.ok_cancel_dialog("You need to be logged in to generate a shareable link",ok_title="Login",title="Pieces"):
				self.window.run_command("pieces_login")
			return 
		if not user.allocation:
			if sublime.ok_cancel_dialog("You need to connect to the cloud to generate a shareable link",ok_title="Connect",title="Pieces"):
				self.window.run_command("pieces_allocation_connect")
			return

		self.thread = LinkifyApi(PiecesSettings.api_client).linkify(async_req=True,
			linkify=Linkify(
				access="PUBLIC",
				**kwargs
				)
			)
		
		share = None
		try:
			share = self.thread.get(120)
			if self.sheet and self.update_sheet:
				if self.sheet.id() in PiecesListAssetsCommand.sheets_md:
					PiecesListAssetsCommand.update_sheet(self.sheet,asset_id,
						{"share":
							{"title":"Copy Generated Link",
							"url":f'subl:pieces_copy_link  {{"content":"{share.iterable[0].link}", "asset_id":"{asset_id}"}}'}
						})

		except:	
			pass

		if share: return share
		

class PiecesGenerateShareableLinkCommand(sublime_plugin.TextCommand):
	def run(self,edit,data=None):
		self.data = data
		sublime.set_timeout_async(self.run_async)


	def run_async(self):
		self.view.set_status("pieces_share","Creating asset")
		create_asset = PiecesCreateAssetCommand(self.view)
		seed = create_asset.get_seeds(self.data)

		self.view.set_status("pieces_share","Generating shareable link")

		shares = PiecesShareAssetCommand(sublime.active_window()).run_async(seed=seed)
		link = shares.iterable[0].link
		self.view.set_status("pieces_share",f"Link Generated {link}")

		# self.show_dialog(link)
		self.create_popup(self.view,link)
		sublime.set_timeout(lambda: self.view.erase_status("pieces_share"),4000)
	

	@staticmethod
	def show_dialog(link):
		if sublime.ok_cancel_dialog(
			f"Link Generated successfully \n{link}",ok_title="Copy",title="Pieces Shareable link"
			):
			sublime.set_clipboard(link)


	@staticmethod
	def create_popup(view:sublime.View,link):
		def on_nav(href):
			nonlocal link
			if href == "copy":
				sublime.set_clipboard(link)
			view.hide_popup()

		css = """
		html.dark {
			--base_background: color(var(--background) blend(white 95%));
			--toolbar: color(var(--base_background) blend(white 95%));
		}

		html.light {
			--base_background: color(var(--background) blend(black 95%));
			--toolbar: color(var(--base_background) blend(black 95%));
		}
		"""
		view.show_popup(
			f"""
			<body>
			<style>{css}</style>
			<div style="background-color:var(--toolbar);margin-bottom:2px">
				<a href="copy">Copy</a> | <a href="dismiss" style="color:var(--redish)">Dismiss</a>
			</div>
			<div style='background-color:var(--base_background)'>Pieces Link Generated: {link}</div>
			</body>""", 
			location=-1,
			on_navigate=on_nav)


class PiecesCopyLinkCommand(sublime_plugin.WindowCommand):
	def run(self,content,asset_id):
		sublime.set_clipboard(content)
		sheet = self.window.active_sheet()
		PiecesListAssetsCommand.update_sheet(sheet,asset_id,buttons_kwargs={"share":{"title":"Copied"}})
