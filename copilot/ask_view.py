import sublime
from .ask_websocket import AskStreamWS
from pieces_os_client import QGPTStreamOutput
from pieces_os_client import QGPTQuestionInput, QGPTStreamInput, RelevantQGPTSeeds
from ..settings import PiecesSettings
from sublime import Region

class CopilotViewManager:
	_gpt_view = None # current view for the ask stream
	_conversation_id = None	
	can_type = True
	
	@property
	def gpt_view(self) -> sublime.View:
		
		if not self._gpt_view:
			CopilotViewManager._gpt_view = sublime.active_window().new_file(syntax="Packages/Markdown/Markdown.sublime-syntax")	
			CopilotViewManager.can_type = True
			self._gpt_view.settings().set("PIECES_GPT_VIEW",True) # Label the view as gpt view
			self._gpt_view.settings().set("end_response",0) # End reponse charater
			self._gpt_view.set_scratch(True)
			self._gpt_view.set_name("Pieces Copilot")
			self._gpt_view.set_status("MODEL",PiecesSettings.model_name)
			self.show_cursor
		return self._gpt_view
		

	@gpt_view.setter
	def gpt_view(self,view):
		self._gpt_view = view

	@property
	def show_cursor(self):
		self.gpt_view.set_status("MODEL",PiecesSettings.model_name)
		self.gpt_view.run_command("append",{"characters":">>> "})
		self.gpt_view.settings().set("end_response",self.end_response+4)  # ">>> " 4 characters
		self.select_end
	
	@property
	def end_response(self) -> int:
		return self.gpt_view.settings().get("end_response")


	def on_message_callback(self,message: QGPTStreamOutput):
		if message.question:
			answers = message.question.answers.iterable

			for answer in answers:
				self.gpt_view.run_command("append",{"characters":answer.text})
		
		if message.status == "COMPLETED":
			self.new_line()
			self.gpt_view.settings().set("end_response",self.gpt_view.size()) # Update the size
			self.show_cursor
			CopilotViewManager.can_type = True
			self._conversation_id = message.conversation

	@property
	def select_end(self) -> None:
		self.gpt_view.run_command('move_to', {"to": "eof"})


	def new_line(self,lines = 2) -> None:
		for _ in range(lines):
			self.gpt_view.run_command("append",{"characters":"\n"})

	def ask(self,relevant=RelevantQGPTSeeds(iterable=[])):
		CopilotViewManager.can_type = False
		self.new_line()
		self.ask_websocket.send_message(
			QGPTStreamInput(
				question=QGPTQuestionInput(
					query = self.gpt_view.substr(Region(self.end_response,self.gpt_view.size())),
					relevant = relevant,
					application=PiecesSettings.get_application().id,
					model = PiecesSettings.model_id
				),
				conversation = self._conversation_id,
				
			))
	
	@property
	def ask_websocket(self):
		if not hasattr(self,"_ask_websocket"):
			CopilotViewManager._ask_websocket = AskStreamWS(self.on_message_callback)
		return self._ask_websocket

	