from ..misc.models_command import ModelsEnum
import sublime
from sublime import ADD_TO_SELECTION, Region, View
from .images.context_image import ContextImage
from .._pieces_lib.pieces_os_client import QGPTStreamOutput
from .._pieces_lib.pieces_os_client.wrapper.basic_identifier.chat import BasicChat
from ..settings import PiecesSettings
from ..progress_bar import ProgressBar
import re


PHANTOM_A_TAG_STYLE = "padding: 4px;background-color: var(--accent); border-radius: 6px;color: var(--foreground);text-decoration: None;text-align: center"

PHANTOM_CONTENT = f"""
<div style="padding-right:2px">
	<a style="{PHANTOM_A_TAG_STYLE}" href ="save_{{id}}">{{save}}</a>
	<a style="{PHANTOM_A_TAG_STYLE}" href="copy_{{id}}">{{copy}}</a>
	<a style="{PHANTOM_A_TAG_STYLE}" href="share_{{id}}">{{share}}</a>
	<a style="{PHANTOM_A_TAG_STYLE}" href="insert_{{id}}">{{insert}}</a>
</div>
"""

FAILED_PHANTOM_CONTENT = f"""
Something went wrong <br><br>
<div style="padding-right:2px;padding-left:2px;padding-buttom:2px">
	<a style="{PHANTOM_A_TAG_STYLE}" href = "retry">Retry</a>
	<a style="{PHANTOM_A_TAG_STYLE}" href = "create">Create a New Conversation</a>
	<a style="{PHANTOM_A_TAG_STYLE}" href = "github">Create a GitHub Issue</a>
	<a style="{PHANTOM_A_TAG_STYLE}" href = "llm">Change current LLM</a>
</div>
"""

class CopilotViewManager:
	def __init__(self):
		self._gpt_view = None
		self._view_name = None
		self._secondary_view = None
		self.progress_bar = ProgressBar("Pieces Copilot")

	@property
	def gpt_view(self) -> View:
		if not self._gpt_view:
			# File config and creation
			self._gpt_view = sublime.active_window().new_file(ADD_TO_SELECTION,syntax="Packages/Markdown/Markdown.sublime-syntax")	
			self.can_type = True
			self._gpt_view.settings().set("PIECES_GPT_VIEW",True) # Label the view as gpt view
			self._gpt_view.settings().set("line_numbers", False) # Remove lines
			self._gpt_view.settings().set("word_wrap",True)
			self._gpt_view.set_scratch(True)

			# Phantom intilization 
			self.last_edit_phantom = 0
			self.phantom_set = sublime.PhantomSet(self._gpt_view, "Pieces_Phantoms")
			self.phantom_details_dict = {} # id: {"code":code,"region":region}



			# Failed regions
			self.failed_regions = []
			self.failed_phantom = sublime.PhantomSet(self._gpt_view, "Pieces_Failed_Phantoms")


			# Context Phantom
			self.context_phantom = sublime.PhantomSet(self._gpt_view, "Pieces_context")

			# Others
			self._relevant = {}
			self.copilot_regions = []
			self.update_status_bar()
			# self.render_copilot_image_phantom(self._gpt_view)

			self.show_cursor

			# Update the Copilot message callback
			PiecesSettings.api_client.copilot.ask_stream_ws.on_message_callback = self.on_message_callback
			PiecesSettings.api_client.copilot._return_on_message = lambda:None # Modify the copilot becaue we will use the on_message_callback
		return self._gpt_view
		
	@property
	def view_name(self):
		name = self._view_name
		if not name:
			name = "New Conversation"

		return "Pieces: " + name
	
	@view_name.setter
	def view_name(self,v):
		self._view_name = v
		self.gpt_view.set_name(self.view_name)
	

	@gpt_view.setter
	def gpt_view(self,view):
		self._gpt_view = view


	def update_status_bar(self):
		if self._gpt_view:
			model = ModelsEnum.get(PiecesSettings.api_client.model_name)
			model = model.name if model else "UNKNOWN"
			self._gpt_view.set_status("MODEL",f"LLM Model: {model}")

	@property
	def show_cursor(self):
		self.update_status_bar()
		region = sublime.Region(self.gpt_view.size(), self.gpt_view.size())
		point_phantom = self.gpt_view.line(region.a).begin()

		self.add_context_phantom(sublime.Region(point_phantom,point_phantom))

		ui = sublime.ui_info()["theme"]["style"]

		self.copilot_regions.append(region)

		# Add the regions with the icon and appropriate flags
		self.gpt_view.add_regions(
			"pieces", 
			self.copilot_regions, 
			scope="text", 
			icon=f"Packages/Pieces/copilot/images/copilot-icon-{ui}.png", 
			flags=sublime.HIDDEN
		)
		self.add_role("User")
		self.select_end
	
	@property
	def end_response(self) -> int:
		return self.gpt_view.settings().get("end_response",0)

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
			self.reset_view()
			self.conversation_id = message.conversation
			self.add_code_phantoms() # Generate the code phantoms	
		elif message.status == "FAILED":
			self.failed_regions.append(self.copilot_regions.pop())
			self.show_failed()
			self.gpt_view.run_command("pieces_clear_line",{"line_point": self.gpt_view.size()})
			self.reset_view()

		if message.status != "IN-PROGRESS":
			self.progress_bar.stop()

	def show_failed(self):
		self.gpt_view.add_regions(
			"pieces", 
			self.failed_regions, 
			scope="region.yellowish", 
			icon=f"Packages/Pieces/copilot/images/warning.png", 
			flags=sublime.HIDDEN
		)
		self.failed_phantom.update(
			[sublime.Phantom(region,FAILED_PHANTOM_CONTENT,sublime.LAYOUT_BLOCK,self.on_nav_failed) for region in self.failed_regions] # TODO: Add retry
		)

	def on_nav_failed(self, href):
		if href == "retry":
			self.add_query(self.prev_query)
			self.gpt_view.run_command("pieces_enter_response")
		elif href == "create":
			self.render_conversation("") # Render a new empty conversation
		elif href == "github":
			sublime.run_command("pieces_support",args={"support": "https://github.com/pieces-app/plugin_sublime/issues"})
		elif href == "llm":
			sublime.active_window().run_command("edit_settings",
            {
                "base_file": f"{sublime.packages_path()}/Pieces/Pieces.sublime-settings",
                "default": "\n{\n\t$0\n}\n"
            }
        )

	def add_context_phantom(self,region):
		self.context_phantom_region = region
		ui = sublime.ui_info()["theme"]["style"]
		if ui not in ["light","dark"]:
			ui = "light"
		image = getattr(ContextImage,ui)
		self.context_phantom.update(
			[sublime.Phantom(region,f"<a href='subl:pieces_context_manager'>{image.format(style='width:20px;height:20px')}</a>",sublime.LAYOUT_INLINE)]
		)
	def remove_context_phantom(self):
		self.context_phantom.update([])

	def reset_view(self):
		self.end_response = self.gpt_view.size()
		self.show_cursor
		self.can_type = True

	@property
	def conversation_id(self):
		return self.gpt_view.settings().get("conversation_id")

	@conversation_id.setter
	def conversation_id(self,id):
		PiecesSettings.api_client.copilot.chat = BasicChat(id) if id else None
		self.gpt_view.settings().set("conversation_id",id)

	@property
	def select_end(self) -> None:
		self.gpt_view.run_command('move_to', {"to": "eof"})


	def new_line(self,lines = 2) -> None:
		for _ in range(lines):
			self.gpt_view.run_command("append",{"characters":"\n"})


	def ask(self,pipeline=None):
		self.prev_query = self.gpt_view.substr(Region(self.end_response,self.gpt_view.size()))
		if not self.prev_query.strip():
			return
		self.can_type = False
		self.select_end # got to the end of the text to enter the new lines
		self.new_line()
		self.remove_context_phantom()
		self.add_role("Copilot")
		self.progress_bar.start()
		sublime.set_timeout_async(lambda: PiecesSettings.api_client.copilot.stream_question(self.prev_query,pipeline))

	def add_role(self,role):
		text = f'>>> **{role}**: '
		self.gpt_view.run_command("append",{"characters":text})
		self.end_response = self.gpt_view.size()
		

	def add_code_phantoms(self):
		view = self.gpt_view

		content = view.substr(sublime.Region(self.last_edit_phantom, view.size()))
		
		# Regular expression to find code blocks in Markdown
		code_block_pattern = re.compile(r'```.*?\n(.*?)```', re.DOTALL)
		matches = code_block_pattern.finditer(content)


		for match in matches:
			id = str(len(self.phantom_details_dict))
			# Create a phantom at the end of each code block

			end_point = match.end()
			region = sublime.Region(end_point+self.last_edit_phantom, end_point+self.last_edit_phantom)
			self.phantom_details_dict[id] = {"code":match.group(1),"region":region}
			self.update_phantom_set(region,id)

		self.last_edit_phantom = view.size()

	def on_nav(self,href:str):
		command,id = href.split("_")
		code = self.phantom_details_dict[id]["code"]
		region = self.phantom_details_dict[id]["region"]
		if command == "save":
			self.gpt_view.run_command("pieces_create_asset",{"data":code})
			self.update_phantom_set(region,id,"Saving")
			sublime.set_timeout_async(lambda:self.update_phantom_set(region,id,"Save"),5000) # TODO: Change it to a view button

		elif command == "copy":
			sublime.set_clipboard(code)
			self.update_phantom_set(region,id,copy="Copied")
			sublime.set_timeout_async(lambda:self.update_phantom_set(region,id,copy="Copy"),5000)
		elif command == "share":
			self.gpt_view.run_command("pieces_generate_shareable_link",{"data":code})
			self.update_phantom_set(region,id,share="Sharing")
			sublime.set_timeout_async(lambda:self.update_phantom_set(region,id),5000)
		elif command == "insert":
			s = self.secondary_view
			if s:
				s.run_command("pieces_insert_text",{"text":code})

	def update_phantom_set(self,region,id,save="Save",copy="Copy",share="Share",insert="Insert",reset = False):
		# Change the text 
		phantom = sublime.Phantom(
				region,
				PHANTOM_CONTENT.format(id = id,copy=copy,save=save,share=share,insert=insert),
				sublime.LAYOUT_BELOW,
				on_navigate=self.on_nav
			)
		
		if not reset:
			phantoms = [phantom for phantom in self.phantom_set.phantoms if phantom.region != region]
			phantoms = [phantom,*phantoms]
		else: 
			phantoms = [phantom]
		self.phantom_set.update(phantoms)



	def render_conversation(self,conversation_id):
		# Clear everything!
		self.clear()

		if conversation_id:
			try:
				self.conversation_id = conversation_id
			except ValueError:
				return sublime.error_message("Conversation not found") # Error conversation not found
		else:
			self.view_name = "New Conversation"
			self.conversation_id = None
			return 
		chat = PiecesSettings.api_client.copilot.chat
		self.gpt_view.run_command("select_all")
		self.gpt_view.run_command("right_delete") # Clear the cursor created by default ">>>"
		self.view_name = chat.name if chat else "New Conversation"

		if chat:
			for message in chat.messages():
				if message.role == "USER":
					self.show_cursor
				else:
					self.add_role("Copilot")
				
				if message.raw_content:
					self.gpt_view.run_command("append",{"characters":message.raw_content})

				self.new_line()

		self.show_cursor
		self.end_response = self.gpt_view.size()
		self.add_code_phantoms()
    
	@property
	def secondary_view(self):
		return self._secondary_view # Will be updated via event listeners

	@secondary_view.setter
	def secondary_view(self,view):
		if not view.settings().get("PIECES_GPT_VIEW") and view in sublime.active_window().views():
			self._secondary_view = view

	def clear(self):
		if self._gpt_view:
			self._gpt_view.close()
			self._gpt_view = None

	def add_query(self,query):
		self.gpt_view.run_command("append",{"characters":query})

