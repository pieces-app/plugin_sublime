import sublime
from .ask_websocket import AskStreamWS
from .conversations import ConversationsSnapshot
from pieces_os_client import ConversationMessageApi, QGPTQuestionInput, QGPTStreamInput, RelevantQGPTSeeds,QGPTStreamOutput
from ..settings import PiecesSettings
from sublime import Region
import re


PHANTOM_A_TAG_STYLE = "padding: 4px;background-color: var(--accent); border-radius: 6px;color: var(--foreground);text-decoration: None;text-align: center"

PHANTOM_CONTENT = f"""
<div style="padding-right:2px">
	<a style="{PHANTOM_A_TAG_STYLE}" href ="save_{{0}}">Save</a>
	<a style="{PHANTOM_A_TAG_STYLE}" href="copy_{{0}}">Copy</a>
</div>
"""

class CopilotViewManager:
	can_type = True
	
	@property
	def gpt_view(self) -> sublime.View:
		if not getattr(CopilotViewManager, "_gpt_view",None):
			# File config and creation
			CopilotViewManager._gpt_view = sublime.active_window().new_file(syntax="Packages/Markdown/Markdown.sublime-syntax")	
			CopilotViewManager.can_type = True
			CopilotViewManager._gpt_view.settings().set("PIECES_GPT_VIEW",True) # Label the view as gpt view
			CopilotViewManager._gpt_view.settings().set("end_response",0) # End reponse charater
			CopilotViewManager._gpt_view.set_scratch(True)
			CopilotViewManager._gpt_view.set_name("Pieces Copilot")

			# Phantom intilization 
			self.last_edit_phantom = 0
			self.phantom_set = sublime.PhantomSet(CopilotViewManager._gpt_view, "Pieces_Phantoms")
			self.code_blocks_dict = {} # id: code


			# Others
			self.show_cursor
			self.update_status_bar()
		return CopilotViewManager._gpt_view
		

	@gpt_view.setter
	def gpt_view(self,view):
		CopilotViewManager._gpt_view = view


	def update_status_bar(self):
		if getattr(self,"_gpt_view",None):
			self._gpt_view.set_status("MODEL",f"LLM Model: {PiecesSettings.model_name.replace('Chat Model','')}")

	@property
	def show_cursor(self):
		self.gpt_view.set_status("MODEL",PiecesSettings.model_name)
		self.gpt_view.run_command("append",{"characters":">>> "})
		self.end_response = self.end_response + 4  # ">>> " 4 characters
		self.select_end
	
	@property
	def end_response(self) -> int:
		return self.gpt_view.settings().get("end_response")

	@end_response.setter
	def end_response(self,e):
		self.gpt_view.settings().set("end_response",e)

	def on_message_callback(self,message: QGPTStreamOutput):
		if message.question:
			answers = message.question.answers.iterable

			for answer in answers:
				self.gpt_view.run_command("append",{"characters":answer.text})
		
		if message.status == "COMPLETED":
			self.new_line()
			self.end_response = self.gpt_view.size() # Update the size
			self.show_cursor
			CopilotViewManager.can_type = True
			self.conversation_id = message.conversation
			self.add_code_phantoms() # Generate the code phantoms
	@property
	def conversation_id(self):
		return self.gpt_view.settings().get("conversation_id")

	@conversation_id.setter
	def conversation_id(self,id):
		self.gpt_view.settings().set("conversation_id",id)

	@property
	def select_end(self) -> None:
		self.gpt_view.run_command('move_to', {"to": "eof"})


	def new_line(self,lines = 2) -> None:
		for _ in range(lines):
			self.gpt_view.run_command("append",{"characters":"\n"})

	def ask(self,relevant=RelevantQGPTSeeds(iterable=[])):
		CopilotViewManager.can_type = False
		self.select_end # got to the end of the text to enter the new lines
		self.new_line()
		self.ask_websocket.send_message(
			QGPTStreamInput(
				question=QGPTQuestionInput(
					query = self.gpt_view.substr(Region(self.end_response,self.gpt_view.size())),
					relevant = relevant,
					application=PiecesSettings.get_application().id,
					model = PiecesSettings.model_id
				),
				conversation = self.conversation_id,
				
			))
	
	@property
	def ask_websocket(self):
		if not hasattr(self,"_ask_websocket"):
			CopilotViewManager._ask_websocket = AskStreamWS(self.on_message_callback)
		return self._ask_websocket



	def add_code_phantoms(self):
		view = self.gpt_view

		content = view.substr(sublime.Region(self.last_edit_phantom, view.size()))
		
		# Regular expression to find code blocks in Markdown
		code_block_pattern = re.compile(r'```.*?\n(.*?)```', re.DOTALL)
		matches = code_block_pattern.finditer(content)
		
		
		phantoms = []

		for match in matches:
			id = str(len(self.code_blocks_dict))
			# Create a phantom at the end of each code block
			self.code_blocks_dict[id] = match.group(1)
			end_point = match.end()
			phantom = sublime.Phantom(
				sublime.Region(end_point+self.last_edit_phantom, end_point+self.last_edit_phantom),
				PHANTOM_CONTENT.format(id),
				sublime.LAYOUT_BELOW,
				on_navigate=self.on_nav
			)
			phantoms.append(phantom)

		self.phantom_set.update(phantoms)

		self.last_edit_phantom = view.size()

	def on_nav(self,href:str):
		command,id = href.split("_")
		code = self.code_blocks_dict[id]

		if command == "save":
			self.gpt_view.run_command("pieces_create_asset",{"data":code})
		elif command == "copy":
			sublime.set_clipboard(code)


	def render_conversation(self,conversation_id):
		self.conversation_id = conversation_id # Set the conversation

		# Clear everything!
		self._gpt_view = None # clear the old _gpt_view

		

		if conversation_id:
			conversation = ConversationsSnapshot.identifiers_snapshot.get(conversation_id)
			if not conversation:
				return sublime.error_message("Conversation not found") # Error conversation not found
		else:
			return # Nothing need to be rendered 
		
		self.gpt_view.run_command("select_all")
		self.gpt_view.run_command("right_delete") # Clear the cursor created by default ">>>"
		
		message_api = ConversationMessageApi(PiecesSettings.api_client)
		first_message = True
		for key,val in conversation.messages.indices.items():
			if val == -1: # message is deleted
				continue
			message = message_api.message_specific_message_snapshot(message=key)
			if message.role == "USER":
				if not first_message:
					self.new_line()
				first_message = False

				self.show_cursor
				

			if message.fragment.string:
				self.gpt_view.run_command("append",{"characters":message.fragment.string.raw})


		self.new_line()
		self.show_cursor
		self.end_response = self.gpt_view.size()
		self.add_code_phantoms()