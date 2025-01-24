import sublime_plugin
import sublime
from .ask_view import CopilotViewManager
from ..settings import PiecesSettings
from ..startup_utils import check_pieces_os
from .._pieces_lib.pieces_os_client.models.qgpt_stream_input import QGPTStreamInput
from .._pieces_lib.pieces_os_client.wrapper.basic_identifier.chat import BasicChat


copilot = CopilotViewManager()


class PiecesAskStreamCommand(sublime_plugin.WindowCommand):
	@check_pieces_os()
	def run(self,pieces_choose_type,pieces_query=None,pieces_conversation_id=None):
		copilot.render_conversation(pieces_conversation_id)
		if pieces_query:
			copilot.add_query(pieces_query)
			self.window.active_view().run_command("pieces_enter_response")
		return

	@check_pieces_os(True)
	def input(self,args):
		return PiecesChooseTypeInputHandler()


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
	def validate(self, text: str) -> bool:
		return bool(text.strip())


class PiecesEnterResponseCommand(sublime_plugin.TextCommand):
	@check_pieces_os()
	def run(self,edit):
		copilot.ask()

class PiecesDeleteConversationCommand(sublime_plugin.WindowCommand):
	@check_pieces_os()
	def run(self, pieces_conversation_id):
		conv = BasicChat(pieces_conversation_id)
		name = conv.name
		conv.delete()
		sublime.status_message(f'The conversation "{name}" has been successfully deleted.')
		sublime.set_timeout(
		# if a user want to delete another conversation
		lambda:self.window.run_command("pieces_delete_conversation"),100) # Wait for some ms

	@check_pieces_os(True)
	def input(self, args: dict):
		return PiecesConversationIdInputHandler()

class PiecesConversationIdInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		return [
			sublime.ListInputItem(
				text=chat.name,
				value=chat.id,
				details=self.get_annotation(chat)) 
			for chat in PiecesSettings.api_client.copilot.chats()]

	def get_annotation(self,chat):
		try:
			annotation = " "
			annotations = chat.conversation.annotations
			if annotations and annotations.indices:
				annotation = PiecesSettings.api_client.annotation_api.annotation_specific_annotation_snapshot(list(annotations.indices.keys())[0]).text.replace("\n"," ")
			return annotation
		except:
			return ""

	def placeholder(self):
		return "Choose a conversation or start new one"

class PiecesInsertTextCommand(sublime_plugin.TextCommand):
	def run(self,edit,text,point=None):
		self.view.window().focus_view(self.view)
		if not point:
			point = self.view.sel()[0].begin()
		self.view.insert(edit,int(point),text)


class PiecesClearLineCommand(sublime_plugin.TextCommand):
	def run(self, edit: sublime.Edit, line_point:int):
		self.view.replace(edit,self.view.line(int(line_point)), "")

class PiecesRemoveRegionCommand(sublime_plugin.TextCommand):
	def run(self, edit: sublime.Edit, a: int,b:int):
		self.view.replace(edit,sublime.Region(a,b), "")

class PiecesStopCopilotCommand(sublime_plugin.TextCommand):
	@check_pieces_os()
	def run(self,edit: sublime.Edit):
		PiecesSettings.api_client.copilot.ask_stream_ws.send_message(
			QGPTStreamInput(
			  conversation = PiecesSettings.api_client.copilot._chat_id,
			  stop = True
			 )
		)
	def is_enabled(self) -> bool:
		return bool(self.view.settings().get("PIECES_GPT_VIEW", False))
