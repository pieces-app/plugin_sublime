from pieces_os_client import AnnotationApi
import sublime_plugin
import sublime
from .ask_view import CopilotViewManager
from .conversations import ConversationsSnapshot
from ..settings import PiecesSettings

copilot = CopilotViewManager()


class PiecesAskStreamCommand(sublime_plugin.WindowCommand):
	def run(self,pieces_conversation_id=None):
		copilot.ask_websocket.start()
		copilot.conversation_id = pieces_conversation_id # Set the conversation
		self.window.focus_view(copilot.gpt_view)
		return

	def input(self,args):
		return PiecesConversationIdInputHandler()

	def is_enabled(self):
		return PiecesSettings().is_loaded


class PiecesEnterResponseCommand(sublime_plugin.TextCommand):
	def run(self,_):
		copilot.ask()

	def is_enabled(self):
		return PiecesSettings().is_loaded



class PiecesConversationIdInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		conversation_list = [
			sublime.ListInputItem(text="Create New Conversation", value=None)
		]
		api = AnnotationApi(PiecesSettings.api_client)
		for conversation in ConversationsSnapshot.identifiers_snapshot.values():
			name = getattr(conversation,"name","New Conversation")
			annotations = conversation.annotations.indices
			details = None
			if annotations:
				details = api.annotation_specific_annotation_snapshot(list(annotations.keys())[0]).text
			conversation_list.append(sublime.ListInputItem(text=name, value=conversation.id,details=details))


		return conversation_list

	def placeholder(self):
		return "Choose an asset"

