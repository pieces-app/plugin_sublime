import sublime_plugin
import sublime
from .ask_view import CopilotViewManager
from .._pieces_lib.pieces_os_client.wrapper.websockets import ConversationWS
from .._pieces_lib.pieces_os_client import AnnotationApi,Seeds,FlattenedAssets
from ..settings import PiecesSettings
from typing import Optional

copilot = CopilotViewManager()


class PiecesAskStreamCommand(sublime_plugin.WindowCommand):
	def run(self,pieces_choose_type,pieces_query=None,pieces_conversation_id=None):
		copilot.render_conversation(pieces_conversation_id)
		if pieces_query:
			copilot.add_query(pieces_query)
			self.window.active_view().run_command("pieces_enter_response")
		return

	def input(self,args):
		return PiecesChooseTypeInputHandler()

	def is_enabled(self):
		return PiecesSettings.is_loaded and ConversationWS.is_running()

class PiecesChooseTypeInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		return [
			("Create New Conversation", "new"),
			# ("Search a Conversation", "search"),
			("View Conversation List","view"),
			("Ask a question","question")
		]
	def next_input(self, args):
		t = args["pieces_choose_type"]
		if t == "search":
			return # TODO: Add searching via endpoint
		elif t == "view":
			return PiecesConversationIdInputHandler()
		elif t == "question":
			return PiecesQueryInputHandler()


class PiecesQueryInputHandler(sublime_plugin.TextInputHandler):
	def placeholder(self) -> str:
		return "Enter a query to ask the copilot about"


class PiecesEnterResponseCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		copilot.ask()

	def is_enabled(self):
		return PiecesSettings.is_loaded


class PiecesConversationIdInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		return [
			sublime.ListInputItem(
				text=chat.name,
				value=chat.id,
				details=chat.description.replace("\n","") if chat.description else "")
		 for chat in PiecesSettings.api_client.copilot.chats()]

	def placeholder(self):
		return "Choose a conversation or start new one"

class PiecesInsertTextCommand(sublime_plugin.TextCommand):
	def run(self,edit,text,point=None):
		self.view.window().focus_view(self.view)
		if not point:
			point = self.view.sel()[0].begin()
		self.view.insert(edit,point,text)