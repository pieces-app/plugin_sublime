import sublime_plugin
import sublime
from .._pieces_lib.pieces_os_client.wrapper.basic_identifier.asset import BasicAsset

from .list_assets import PiecesListAssetsCommand
from ..settings import PiecesSettings
from ..startup_utils import check_pieces_os
from ..auth.auth_user import AuthUser


class PiecesShareAssetCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		self.sheet = None
		self.update_sheet = False # Should we update the current sheet
		super().__init__(window)

	@check_pieces_os()
	def run(self,asset_id,update_sheet=False):
		self.update_sheet = update_sheet
		self.sheet = self.window.active_sheet()
		if update_sheet:
			PiecesListAssetsCommand.update_sheet(self.sheet,asset_id,{"share":{"title":"Sharing","url":"noop"}})
		sublime.set_timeout_async(lambda:self.run_async(asset_id))

	def run_async(self,asset_id=None,raw_content=None):
		"""
			You need to either give the seed or the asset_id
		"""
		user = AuthUser.user_profile
		if not user:
			if sublime.ok_cancel_dialog("You need to be logged in to generate a shareable link",ok_title="Login",title="Pieces"):
				self.window.run_command("pieces_login")
			return 
		if not user.allocation:
			if sublime.ok_cancel_dialog("You need to connect to the cloud to generate a shareable link",ok_title="Connect",title="Pieces"):
				self.window.run_command("pieces_allocation_connect")
			return
		try:
			if asset_id:
				share = BasicAsset(asset_id).share()
			if raw_content:
				share = BasicAsset.share_raw_content(raw_content)
		except:
			return sublime.error_message("Unable to create a shareable link")

		if self.sheet and self.update_sheet:
			if self.sheet.id() in PiecesListAssetsCommand.sheets_md:
				PiecesListAssetsCommand.update_sheet(self.sheet,asset_id,
					{"share":
						{"title":"Copy Generated Link",
						"url":f'subl:pieces_copy_link  {{"content":"{share.iterable[0].link}", "asset_id":"{asset_id}"}}'}
					})
		PiecesSettings.notify("Shareable Link Generated",share.iterable[0].link)
		return share

		

class PiecesGenerateShareableLinkCommand(sublime_plugin.TextCommand):
	@check_pieces_os()
	def run(self,edit,data=None):
		self.data = data
		if not data:
			self.data = "\n".join([self.view.substr(selection) for selection in self.view.sel()])
			if not self.data:
				return sublime.error_message("Please select a text")
		sublime.set_timeout_async(self.run_async)


	def run_async(self):
		self.view.set_status("pieces_share","Creating asset")

		self.view.set_status("pieces_share","Generating shareable link")

		shares = PiecesShareAssetCommand(sublime.active_window()).run_async(raw_content=self.data)
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
			on_navigate=on_nav,
			max_width=350)


class PiecesCopyLinkCommand(sublime_plugin.WindowCommand):
	@check_pieces_os()
	def run(self,content,asset_id):
		sublime.set_clipboard(content)
		sheet = self.window.active_sheet()
		PiecesListAssetsCommand.update_sheet(sheet,asset_id,buttons_kwargs={"share":{"title":"Copied","url":"noop"}})

