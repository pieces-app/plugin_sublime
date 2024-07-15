import sublime
import sublime_plugin

from .assets.list_assets import PiecesListAssetsCommand
from .assets.ext_map import file_map
from .assets.assets_snapshot import AssetSnapshot
from .settings import PiecesSettings
from .misc import PiecesOnboardingCommand
from .copilot.ask_command import copilot
from .copilot.ask_view import CopilotViewManager
from .copilot.conversation_websocket import ConversationWS


file_map_reverse = {v:k for k,v in file_map.items()}


class PiecesEventListener(sublime_plugin.EventListener):
	secondary_view = None # Used in the ask to know the ssecondary view at insert
	commands_to_exclude = ["pieces_onboarding","pieces_reload","pieces_support"]

	onboarding_commands_dict = {
		"pieces_create_asset":"create",
		"pieces_list_assets":"open",
		"pieces_ask_question":"ask",
		"pieces_search":"search",
		"pieces_ask_stream":"copilot",
		"pieces_share_asset":"share",
		"pieces_explain":"explain"
	}
	def on_post_text_command(self,window,command_name,args):
		self.check_onboarding(command_name)
	def on_post_window_command(self,window,command_name,args):
		self.check_onboarding(command_name)
	def on_window_command(self, window, command_name, args):
		self.check(command_name)
		
	def on_text_command(self,view,command_name,args):
		self.check(command_name)

		if command_name == "paste": # To avoid pasting in the middle of the view of the copilot
			self.on_query_context(view,"pieces_copilot_add",True,sublime.OP_EQUAL,True)
		elif command_name == "cut":
			self.on_query_context(view,"pieces_copilot_remove",True,sublime.OP_EQUAL,True)

	def check(self,command_name):
		if command_name.startswith("pieces_") and command_name not in PiecesEventListener.commands_to_exclude: # Check any command 
			health = PiecesSettings.get_health()
			if not health:
				PiecesSettings.is_loaded = False
				sublime.message_dialog("The Pieces OS server is not running")
				return False
		return None
	
	def check_onboarding(self,command_name):
		if command_name not in self.onboarding_commands_dict:
			return
		PiecesOnboardingCommand.add_onboarding_settings(**{self.onboarding_commands_dict[command_name] : True})

	def on_pre_close(self,view):
		sheet_id = view.settings().get("pieces_sheet_id","")
		if sheet_id in PiecesListAssetsCommand.sheets_md:
			asset_id = PiecesListAssetsCommand.sheets_md[sheet_id]
			asset_wrapper = AssetSnapshot(asset_id)
			code = asset_wrapper.get_asset_raw()
			data = view.substr(sublime.Region(0, view.size()))
			
			if data != code:
				sublime.active_window().focus_view(view)
				if sublime.ok_cancel_dialog("Do you want to this snippet to pieces?", ok_title='Save', title='Save snippet'):
					view.window().run_command("pieces_handle_markdown",{"mode": "save","sheet_id":sheet_id,"data":data,"close":False})
					del view.settings()["pieces_sheet_id"]
					return
			sublime.active_window().run_command("pieces_list_assets",{"pieces_asset_id":asset_id})



	def on_query_context(self,view,key, operator, operand, match_all):
		if key == "save_pieces_asset":
			return view.settings().get("pieces_sheet_id")
	
		elif key == "PIECES_GPT_VIEW":
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
				# Update the conversation to be real-time
				# Close the old view and rerender the conversation
				conversation = view.settings().get("conversation_id")
				if conversation:
					on_open = lambda: view.close(lambda x:copilot.render_conversation(conversation)) # Wait some sec until the conversations is loaded
					if ConversationWS.is_running():
						on_open() # Run the command if it is running already
					else: 
						instance = ConversationWS.get_instance()
						if instance:
							instance.on_open_callbacks.append(on_open)
	@staticmethod
	def on_deactivated(view):
		copilot.secondary_view = view

	def on_query_completions(self, view:sublime.View, prefix, locations):
		syntax = view.syntax()
		if not syntax:
			return
		classification_enum = file_map_reverse.get(syntax.path)
		out = []
		for asset_id in AssetSnapshot.identifiers_snapshot:
			asset_wrapper = AssetSnapshot(asset_id)
			if asset_wrapper.original_classification_specific() == classification_enum:
				content = asset_wrapper.get_asset_raw()
				
				if prefix.lower() in asset_wrapper.name.lower().replace(" ","") and prefix != "":
					href = sublime.command_url("pieces_show_completion_details",{"asset_id":asset_wrapper._asset_id})
					out.append(
						sublime.CompletionItem(
							asset_wrapper.name,
							annotation="Pieces",
							completion=content,
							kind=sublime.KIND_SNIPPET,
							details=f"<div><a href='{href}'>More </a></div>")
						)
		return sublime.CompletionList(out)


class PiecesViewEventListener(sublime_plugin.ViewEventListener):
	def on_close(self):
		if self.view.settings().get("PIECES_GPT_VIEW"):
			copilot.gpt_view = None

