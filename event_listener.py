import sublime
import sublime_plugin

from .assets.list_assets import PiecesListAssetsCommand
from .settings import PiecesSettings


class PiecesEventListener(sublime_plugin.EventListener):
	commands_to_exclude = ["pieces_handle_markdown","pieces_reload","pieces_support"]

	def on_window_command(self, window, command_name, args):
		self.check(command_name)
		
	def on_text_command(self,view,command_name,args):
		self.check(command_name)
		if command_name == "save":
			return ("pieces_handle_markdown","save")

	def check(self,command_name):
		if command_name.startswith("pieces_") and command_name not in PiecesEventListener.commands_to_exclude: # Check any command 
			health = PiecesSettings.get_health()
			if not health:
				PiecesSettings.is_loaded = False
				sublime.message_dialog("The Pieces OS server is not running")
				return False
		return None
	

	def on_pre_close(self,view):
		sheet_id = view.settings().get("pieces_sheet_id")
		if sheet_id and sheet_id in PiecesListAssetsCommand.sheets_md:
			code = PiecesListAssetsCommand.sheets_md[sheet_id].get("code")
			asset_id = PiecesListAssetsCommand.sheets_md[sheet_id].get("id")
			data = view.substr(sublime.Region(0, view.size()))
			if code == data:
				return
			
			if sublime.ok_cancel_dialog("Do you want to this snippet to pieces?", ok_title='Save', title='Save snippet'):
				view.window().run_command("pieces_handle_markdown",{"mode": "save","sheet_id":sheet_id})
				view.close(on_close=lambda x:sublime.active_window().run_command("pieces_list_assets",{"pieces_asset_id":asset_id}))
				return

	def on_query_context(self,view,key, operator, operand, match_all):
		if view.settings().get("pieces_sheet_id") and key == "pieces_save_asset":
			self.on_pre_close(view)
			return True