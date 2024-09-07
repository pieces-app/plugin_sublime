import sublime
from sublime import Region
from .images.context_image import ContextImage
from .._pieces_lib.pieces_os_client import QGPTStreamOutput
from .._pieces_lib.pieces_os_client.wrapper.basic_identifier.chat import BasicChat
from ..settings import PiecesSettings
import re
from typing import Optional


PHANTOM_A_TAG_STYLE = "padding: 4px;background-color: var(--accent); border-radius: 6px;color: var(--foreground);text-decoration: None;text-align: center"

PHANTOM_CONTENT = f"""
<div style="padding-right:2px">
	<a style="{PHANTOM_A_TAG_STYLE}" href ="save_{{id}}">{{save}}</a>
	<a style="{PHANTOM_A_TAG_STYLE}" href="copy_{{id}}">{{copy}}</a>
	<a style="{PHANTOM_A_TAG_STYLE}" href="share_{{id}}">{{share}}</a>
	<a style="{PHANTOM_A_TAG_STYLE}" href="insert_{{id}}">{{insert}}</a>
</div>
"""

class CopilotViewManager:
	can_type = True
	_gpt_view = None

	@property
	def gpt_view(self) -> sublime.View:
		if not getattr(CopilotViewManager, "_gpt_view",None):
			# File config and creation
			CopilotViewManager._gpt_view = sublime.active_window().new_file(syntax="Packages/Markdown/Markdown.sublime-syntax")	
			CopilotViewManager.can_type = True
			CopilotViewManager._gpt_view.settings().set("PIECES_GPT_VIEW",True) # Label the view as gpt view
			CopilotViewManager._gpt_view.settings().set("end_response",0) # End reponse charater
			CopilotViewManager._gpt_view.settings().set("line_numbers", False) # Remove lines
			CopilotViewManager._gpt_view.set_scratch(True)
			CopilotViewManager._gpt_view.set_name(self.view_name)

			# Phantom intilization 
			self.last_edit_phantom = 0
			self.phantom_set = sublime.PhantomSet(CopilotViewManager._gpt_view, "Pieces_Phantoms")
			self.phantom_details_dict = {} # id: {"code":code,"region":region}



			# Failed regions
			self.failed_regions = []
			self.failed_phantom = sublime.PhantomSet(CopilotViewManager._gpt_view, "Pieces_Failed_Phantoms")


			# Context Phantom
			self.context_phantom = sublime.PhantomSet(CopilotViewManager._gpt_view, "Pieces_context")

			# Others
			CopilotViewManager._relevant = {}
			self.copilot_regions = []
			self.show_cursor
			self.update_status_bar()
			# self.render_copilot_image_phantom(CopilotViewManager._gpt_view)

        
			# Create a new group (split view)
			sublime.active_window().run_command("set_layout", {
			    "cols": [0.0, 0.5, 1.0],
			    "rows": [0.0, 1.0],
			    "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
			})

			# Move the active view to the new group
			sublime.active_window().set_view_index(CopilotViewManager._gpt_view, 1, 0)

			# Focus on the new group
			sublime.active_window().focus_group(1)

			# Update the Copilot message callback
			PiecesSettings.api_client.copilot.ask_stream_ws.on_message_callback = self.on_message_callback

		return CopilotViewManager._gpt_view
		
	@property
	def view_name(self):
		name = getattr(self,"_view_name","New Conversation")
		if not name:
			name = "New Conversation"

		return "Pieces: " + name
	
	@view_name.setter
	def view_name(self,v):
		self._view_name = v
		self.gpt_view.set_name(self.view_name)
	

	@gpt_view.setter
	def gpt_view(self,view):
		CopilotViewManager._gpt_view = view


	def update_status_bar(self):
		if getattr(self,"_gpt_view",None):
			self._gpt_view.set_status("MODEL",f"LLM Model: {PiecesSettings.api_client.model_name.replace('Chat Model','')}")

	@property
	def show_cursor(self):
		self.update_status_bar()
		self.gpt_view.run_command("append",{"characters":">>> "})
		self.end_response += 4 # ">>> " 4 characters
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
		self.add_role("User: ")
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
			self.reset_view()
			self.conversation_id = message.conversation
			self.add_code_phantoms() # Generate the code phantoms	
		elif message.status == "FAILED":
			self.failed_regions.append(self.copilot_regions.pop())
			self.show_failed()
			self.reset_view()


	def show_failed(self):
		self.gpt_view.add_regions(
			"pieces", 
			self.failed_regions, 
			scope="region.yellowish", 
			icon=f"Packages/Pieces/copilot/images/warning.png", 
			flags=sublime.HIDDEN
		)
		self.failed_phantom.update(
			[sublime.Phantom(region,"Something went wrong",sublime.LAYOUT_BLOCK) for region in self.failed_regions] # TODO: Add retry
		)

	def add_context_phantom(self,region):
		self.context_phantom_region = region
		href = sublime.html_format_command("show_overlay", args={"overlay": "command_palette","text":"Pieces: Manage Conversation Context"})
		ui = sublime.ui_info()["theme"]["style"]
		image = getattr(ContextImage,ui)
		self.context_phantom.update(
			[sublime.Phantom(region,f"<a href='subl:{href}'>{image.format(style='width:20px;height:20px')}</a>",sublime.LAYOUT_INLINE)]
		)
	def remove_context_phantom(self):
		self.context_phantom.update([])

	def reset_view(self):
		self.show_cursor
		CopilotViewManager.can_type = True

	@property
	def conversation_id(self):
		return self.gpt_view.settings().get("conversation_id")

	@conversation_id.setter
	def conversation_id(self,id):
		PiecesSettings.api_client.copilot.chat = BasicChat(id)
		self.gpt_view.settings().set("conversation_id",id)

	@property
	def select_end(self) -> None:
		self.gpt_view.run_command('move_to', {"to": "eof"})


	def new_line(self,lines = 2) -> None:
		for _ in range(lines):
			self.gpt_view.run_command("append",{"characters":"\n"})

	def ask(self,pipeline=None):
		query = self.gpt_view.substr(Region(self.end_response,self.gpt_view.size()))
		if not query:
			return
		CopilotViewManager.can_type = False
		self.select_end # got to the end of the text to enter the new lines
		self.new_line()
		self.remove_context_phantom()
		self.add_role("Copilot")
		sublime.set_timeout_async(lambda: PiecesSettings.api_client.copilot.stream_question(query,pipeline))

	def add_role(self,role):
		self.gpt_view.run_command("append",{"characters":f"{role}: "})
		self.end_response += len(role) + 2

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
				conversation = BasicChat(conversation_id)
				conversation.conversation
			except ValueError:
				return sublime.error_message("Conversation not found") # Error conversation not found
		else:
			self.gpt_view # Nothing need to be rendered 
			if hasattr(self,"_view_name"): delattr(self,"_view_name")
			return 
		
		self.view_name = conversation.name
		self.gpt_view.run_command("select_all")
		self.gpt_view.run_command("right_delete") # Clear the cursor created by default ">>>"


		for message in conversation.messages():
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
		return getattr(self,"_secondary_view",None) # Will be updated via event listeners

	@secondary_view.setter
	def secondary_view(self,view):
		if not view.settings().get("PIECES_GPT_VIEW") and view in sublime.active_window().views():
			self._secondary_view = view

	def clear(self):
		self.end_response = 0
		self.conversation_id = None
		self.can_type = True
		view = self._gpt_view
		self._gpt_view = None
		self.phantom_set.update([])
		if not view:
			return  
		view.run_command("select_all")
		view.run_command("delete")
		self.gpt_view

	def add_query(self,query):
		self.gpt_view.run_command("append",{"characters":query})

