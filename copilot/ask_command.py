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
		self.window.focus_view(copilot.gpt_view)
		copilot.render_conversation(pieces_conversation_id)
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
			if not name: name = "New Conversation"

			try:
				id = list(conversation.annotations.indices.keys())[0]
				details = str(api.annotation_specific_annotation_snapshot(id).text).replace("\n"," ")
			except AttributeError:
				details = ""


			conversation_list.append(sublime.ListInputItem(text=name, value=conversation.id,details=details))

		return conversation_list

	def placeholder(self):
		return "Choose an asset"

