import sublime
import sublime_plugin

from .assets.markdown_handler import PiecesHandleMarkdownCommand
from .assets.list_assets import PiecesListAssetsCommand
from .settings import PiecesSettings
from .misc import PiecesOnBoardingHandlerCommand


class PiecesEventListener(sublime_plugin.EventListener):
	commands_to_exclude = ["pieces_handle_markdown","pieces_reload"
							,"pieces_support","pieces_onboarding"]

	onboarding_commands_dict = {
		"pieces_search":"create_asset",
		"pieces_serach":"search"
	}

	def on_window_command(self, window, command_name, args):
		self.check(command_name)
		self.check_onboarding(command_name)
		
	def on_text_command(self,view,command_name,args):
		self.check(command_name)
		self.check_onboarding(command_name)
			

	def check(self,command_name):
		if command_name.startswith("pieces_") and command_name not in PiecesEventListener.commands_to_exclude: # Check any command 
			health = PiecesSettings.get_health()
			if not health:
				PiecesSettings.is_loaded = False
				sublime.message_dialog("The pieces os server is not running")
				return False
		return None
	
	def check_onboarding(self,command_name):
		if command_name not in self.onboarding_commands_dict:
			return
		PiecesOnBoardingHandlerCommand.add_onboarding_settings(**{self.onboarding_commands_dict[command_name] : True})

	def on_pre_close(self,view):
		asset_id = PiecesHandleMarkdownCommand.views_to_handle.get(view.id())
		if asset_id:
			sheet_details = PiecesListAssetsCommand.sheets_md
			if view.id() not in PiecesHandleMarkdownCommand.saved_asset_view:
				if sublime.ok_cancel_dialog("Do you want to this snippet to pieces?", ok_title='Save', title='Save snippet'):
					view.window().run_command("pieces_handle_markdown",{"mode": "save"})
					return
			view.window().run_command("pieces_list_assets",{"pieces_asset_id":asset_id})
	
	def on_activated(self,view):
		if view.settings().to_dict().get("pieces_onboarding",False):
			view.run_command("pieces_on_boarding_handler")
