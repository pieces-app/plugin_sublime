from typing import Dict
import sublime_plugin
import sublime
from .ask_view import CopilotViewManager
from ..settings import CopilotMode, PiecesSettings
from ..startup_utils import check_pieces_os
from ..progress_bar import ProgressBar
from .._pieces_lib.pieces_os_client.models.qgpt_stream_input import QGPTStreamInput
from .._pieces_lib.pieces_os_client.wrapper.basic_identifier.chat import BasicChat
from .._pieces_lib.pieces_os_client.models.inactive_os_server_applet import InactiveOSServerApplet, OSAppletEnum
from .._pieces_lib.pieces_os_client.models.annotation_type_enum import AnnotationTypeEnum
from .._pieces_lib.pieces_os_client.models.conversation import Conversation

copilot = CopilotViewManager()


class PiecesAskStreamCommand(sublime_plugin.WindowCommand):
	@check_pieces_os()
	def run(self,pieces_choose_type = None,pieces_query=None,pieces_conversation_id = None, mode = None):
		if mode:
			mode = CopilotMode.parse(mode)
		else:
			mode = PiecesSettings.copilot_mode

		if mode.name == CopilotMode.BROWSER.name:
			return PiecesSettings.open_website(
				"localhost:" + str(PiecesSettings.api_client.os_api.os_applet_launch(
								InactiveOSServerApplet(
									type=OSAppletEnum.COPILOT
								)
							).port)
			)
		else:
			copilot.render_conversation(pieces_conversation_id)
			if pieces_query:
				copilot.add_query(pieces_query)
				self.window.active_view().run_command("pieces_enter_response")

	@check_pieces_os(True)
	def input(self,args):
		mode = args.get("mode", PiecesSettings.copilot_mode)
		if isinstance(mode, str):
			mode = CopilotMode.parse(mode)
		if mode.name == CopilotMode.IDE.name:
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
		sublime.set_timeout_async(lambda: self.run_async(pieces_conversation_id))

	def run_async(self, id):
		pb = ProgressBar("Deleting chat")
		pb.start()
		conv = BasicChat(id)
		name = conv.name
		conv.delete()
		pb.stop(f'The conversation "{name}" has been successfully deleted.')
		sublime.set_timeout(
		# if a user want to delete another conversation
		lambda:self.window.run_command("pieces_delete_conversation"),100) # Wait for some ms

	@check_pieces_os(True)
	def input(self, args: dict):
		return PiecesConversationIdInputHandler()

class PiecesConversationIdInputHandler(sublime_plugin.ListInputHandler):
	annotation_cache: Dict[str, str] = {} # Asset ID: annotation description
	def list_items(self):
		return [
			sublime.ListInputItem(
				text=chat.name,
				value=chat.id,
				details=self.get_annotation(chat)) 
			for chat in PiecesSettings.api_client.copilot.chats()]

	def get_annotation(self,chat):
		return self.annotation_cache.get(chat.id, "")

	def placeholder(self):
		return "Choose a chat or start new one"

	@classmethod
	def cache_annotation(cls, conversation: Conversation):
		annotation_list = BasicChat(conversation.id).annotations
		a = annotation_list[0].raw_content if annotation_list else ""
		for annotation in annotation_list:
			if annotation.type == AnnotationTypeEnum.DESCRIPTION:
				a = annotation.raw_content.replace("\n", " ")

		cls.annotation_cache[conversation.id] = a


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
