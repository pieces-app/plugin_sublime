import sublime
import sublime_plugin
import pieces_os_client as pos_client
import re
from difflib import Differ 
import mdpopups
import time

from ..settings import PiecesSettings
from .prompts import *

prompt_map = {"bug":BUGS_PROMPT,
"refactor": CLEANER_CODE_PROMPT,
"docstring":DOC_STRING_PROMPT,
"comment":ADD_COMMENTS_PROMPT}




class PiecesAskQuestionCommand(sublime_plugin.TextCommand):
	def is_enabled(self):
		return PiecesSettings().is_loaded


	def run(self,edit, question):
		sublime.set_timeout_async(lambda:self.run_async(edit,question),0)

		
		

	def run_async(self,edit,question):
		self.question = prompt_map[question]
		
		# Get the current selection
		self.selection = self.view.sel()[0]
		self.selected_text = self.view.substr(self.selection)
		
		try:
			self.langauge = self.view.file_name().split(".")[-1]
		except:
			self.langauge = "txt"

		if not self.selected_text:
			sublime.error_message("Please select a text to ask about!")
			return 

		if self.question in description_needed_commands:
			sublime.active_window().show_input_panel("Enter a description:", "", self.on_done, None, None)
		else:
			self.on_done_async()



	def on_done(self,description):
		self.description = description
		sublime.set_timeout_async(self.on_done_async,0)

	def on_done_async(self):
		self.view.set_status('Pieces Refactoring', 'Copilot is thinking...')

		query = self.question.format(description=self.description,code=self.selected_text) if self.description else self.question.format(code=self.selected_text)
		


		res = pos_client.QGPTApi(PiecesSettings.api_client).question(
			pos_client.QGPTQuestionInput(
				query = query,
				model = PiecesSettings.model_id,
				relevant = pos_client.RelevantQGPTSeeds(
					iterable = [
					# TODO: Use the pipeline prompts
					#     pos_client.RelevantQGPTSeed(
					#         seed = pos_client.Seed(
					#             type="SEEDED_ASSET",
					#             asset=pos_client.SeededAsset(
					#                 application=PiecesSettings.application,
					#                 format=pos_client.SeededFormat(
					#                     fragment = pos_client.SeededFragment(
					#                         string = pos_client.TransferableString(raw = selected_text)
					#                     ),
					#                 ),
					#             ), 
					#         ),
					#     )
					]
				)
			)
		)

		self.view.set_status('Pieces Refactoring', 'Copilot analyzing...')
		self.window  = self.view.window()
		response_code = res.answers.iterable[0].text
		
		# Regular expression pattern for code block
		pattern = r'```.*?\n(.*?)```'

		# Find all matches in the markdown text
		match = re.search(pattern, response_code, re.DOTALL)
		if match:
			self.code = match.group(1)
			self.code_html = self.get_differences(self.selected_text.splitlines(),self.code.splitlines())
			link = "<a href=insert>✅ Accept</a> | <a href=dismiss style='color:red'>❌ Reject</a>"
			html = f"<div style='display:inline-block'>{link}</div>{self.code_html}"

			# Calculate the length of the code_html
			code_html_length = len(self.code_html)

			# Create a phantom at the end of the current selection
			phantom_region = sublime.Region(self.selection.begin(), self.selection.begin() + code_html_length)
			self.phantom = mdpopups.add_phantom(self.view,"code_phantom", phantom_region, html, sublime.LAYOUT_INLINE,md=False,on_navigate=self.on_nav)
			self.is_done = True
			self.view.erase_status('Pieces Refactoring')


	def on_nav(self, href):
		if href == "insert":
			# Replace the selected text with the code
			self.view.run_command("replace_selection", {"code": self.code, "selection": [self.selection.a, self.selection.b]})
			# Remove the phantom
			mdpopups.erase_phantom_by_id(self.view,self.phantom)
		elif href == "dismiss":
			mdpopups.erase_phantom_by_id(self.view,self.phantom)

		


	def get_differences(self,s1:list,s2:list):

	    # Compare the snippets
		diffs = Differ().compare(s1, s2)

		final_output = "\n".join(diffs)
			
		final_output = mdpopups.md2html(self.view,f"```{self.langauge}\n{final_output}\n```")

		return final_output


class ReplaceSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit, code, selection):
        # Convert the selection into a Region
        region = sublime.Region(selection[0], selection[1])

        # Replace the current selection with the provided code
        self.view.replace(edit, region, code)


