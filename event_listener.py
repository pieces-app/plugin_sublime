import sublime
import sublime_plugin
from pieces.api import get_health

from pieces.assets.markdown_handler import PiecesHandleMarkdownCommand



class PiecesEventListener(sublime_plugin.EventListener):
	def on_window_command(self, view, command_name, args):
		
		# List of commands to check
		commands_to_check = ['pieces_list_assets',"pieces_delete_asset"]
		self.check(command_name,commands_to_check)
		
	def on_text_command(self,view,command_name,args):
		commands_to_check = ['pieces_create_asset',"pieces_ask_question"]
		self.check(command_name,commands_to_check)

	def check(self,command_name,commands_to_check):
		if command_name in commands_to_check:
			if not get_health():
				sublime.message_dialog("The pieces os server is not running")
				return False
		return None
	def on_pre_close(self,view):
		asset_id = PiecesHandleMarkdownCommand.views_to_handle.get(view.id())
		if asset_id:
			if view.is_dirty(): # There is unsaved changes
				if sublime.ok_cancel_dialog("Do you want to this snippet to pieces?", ok_title='Save', title='Save snippet'):
					view.window().run_command("pieces_handle_markdown",{"mode": "save"})
					return
			view.window().run_command("pieces_list_assets",{"pieces_asset_id":asset_id})