import sublime
import sublime_plugin

from .assets.markdown_handler import PiecesHandleMarkdownCommand
from .assets.list_assets import PiecesListAssetsCommand
from .settings import PiecesSettings
from .base_websocket import BaseWebsocket
from .copilot.ask_command import copilot


class PiecesEventListener(sublime_plugin.EventListener):
	commands_to_exclude = ["pieces_handle_markdown","pieces_reload","pieces_support"]

	def on_window_command(self, window, command_name, args):
		self.check(command_name)
		
	def on_text_command(self,view,command_name,args):
		self.check(command_name)

	def check(self,command_name):
		if command_name.startswith("pieces_") and command_name not in PiecesEventListener.commands_to_exclude: # Check any command 
			health = PiecesSettings.get_health()
			if not health:
				PiecesSettings.is_loaded = False
				sublime.message_dialog("The pieces os server is not running")
				return False
		return None
	


	def on_pre_close(self,view):
		asset_id = PiecesHandleMarkdownCommand.views_to_handle.get(view.id())
		if asset_id:
			sheet_details = PiecesListAssetsCommand.sheets_md
			if view.id() not in PiecesHandleMarkdownCommand.saved_asset_view:
				if sublime.ok_cancel_dialog("Do you want to this snippet to pieces?", ok_title='Save', title='Save snippet'):
					view.window().run_command("pieces_handle_markdown",{"mode": "save"})
					return
			view.window().run_command("pieces_list_assets",{"pieces_asset_id":asset_id})


	def on_query_context(self,view,key, operator, operand, match_all):
		if key == "PIECES_GPT_VIEW":
			return view.settings().get("PIECES_GPT_VIEW")

		elif key == "pieces_copilot_add" or key == "pieces_copilot_remove":
			## TRUE -> Means no operation will be done
			## False -> Means operation can be done

			if view.settings().get("PIECES_GPT_VIEW"):
				if not copilot.can_type:
					return True # If we can't type then don't accpet operations

				# Set the selection at the begining if we are in the middle of a view
				if copilot.end_response > view.sel()[0].begin():
					copilot.select_end
				

				# Mange the remove to avoid removing the main reponse
				if key == "pieces_copilot_remove" and copilot.end_response >= view.sel()[0].begin():
					return True

				elif key == "pieces_copilot_add" and copilot.end_response > view.sel()[0].begin():
					return True
					
				return False # All cheks is done you can enter what you want!
			else: 
				return False

	def on_init(self,views):
		for view in views:
			if view.settings().get("PIECES_GPT_VIEW"):
				copilot.gpt_view = view # Set the old views

class PiecesViewEventListener(sublime_plugin.ViewEventListener):
	def on_close(self):
		if self.view.settings().get("PIECES_GPT_VIEW"):
			copilot.gpt_view = None