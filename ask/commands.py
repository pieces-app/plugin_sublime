import sublime
import sublime_plugin
import pieces_os_client as pos_client
from pieces.settings import PiecesSettings
import re
from difflib import Differ 
from .prompts import *
import mdpopups
import time

LIST_ITEMS = [
	("Ask for bugs fix",BUGS_PROMPT),
	("Ask for possible bugs", POSSIBLE_BUGS_PROMPT),
	("Write Cleaner code", CLEANER_CODE_PROMPT),
	("Add a doc string to this function",DOC_STRING_PROMPT)
] # TODO: Add more suff 


class DescriptionInputHandler(sublime_plugin.TextInputHandler):
	def placeholder(self):
		return "Enter a quick description of the bug itself or useful error message"
	def validate(self, text):
		return len(text) > 0

class QuestionInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		return LIST_ITEMS
	def next_input(self,args):
		if args in description_needed_commands:
			return DescriptionInputHandler()




class PiecesAskQuestionCommand(sublime_plugin.TextCommand):

	def run(self,edit, question, description=None):
		sublime.set_timeout_async(lambda:self.run_async(edit,question,description),0)

		self.view.set_status('Pieces Refactoring', 'Copilot is thinking...')
		

	def run_async(self,edit, question, description):
		# Get the current selection
		self.selection = self.view.sel()[0]
		selected_text = self.view.substr(self.selection)
		
		if "." in self.view.file_name():
			self.langauge = self.view.file_name().split(".")[-1]
		else: 
			self.langauge = "txt"

		if not selected_text:
			return # TODO show error

		if question in description_needed_commands:
			query = question.format(description=description,code=selected_text)
		else:
			query = question.format(code=selected_text)
		self.view.set_status('Pieces Refactoring', 'Copilot analyzing...')
		res = pos_client.QGPTApi(PiecesSettings.api_client).question(
			pos_client.QGPTQuestionInput(
				query = query,
				model = PiecesSettings.model_id,
				relevant = pos_client.RelevantQGPTSeeds(
					iterable = [
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
		self.view.set_status('Pieces Refactoring', 'Copilot finalizing...')
		self.window  = self.view.window()
		response_code = res.answers.iterable[0].text
		
		# Regular expression pattern for code block
		pattern = r'```.*?\n(.*?)```'

		# Find all matches in the markdown text
		match = re.search(pattern, response_code, re.DOTALL)
		if match:
			self.code = match.group(1)
			self.code_html = self.get_differences(selected_text.splitlines(),self.code.splitlines())
			link = "<a href=insert>✅ Accept</a> | <a href=insert style='color:red'>❌ Reject</a>"
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

			
	def input(self,args):
		return QuestionInputHandler()


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


# class SnippetDifferences:
# 	def __init__(self, previous_state: list, current_state: list):
# 		self.previous_state = previous_state
# 		self.current_state = current_state
# 		self.output = ""

# 	def get_differences(self):
# 		while self.previous_state and self.current_state:

# 			if self.previous_state[0] == self.current_state[0]:
# 				# No changes to the lines
# 				self.output += self.previous_state.pop(0)
# 				self.current_state.pop(0)


# 			elif self.previous_state[0] in self.current_state:
# 				self.handle_line_added_or_modified()
# 			else:
# 				self.handle_line_removed()


# 	def handle_line_added_or_modified(self):
# 		current_idx = 0
# 		while self.previous_state[current_idx] != self.current_state[0]:
# 			matches = difflib.get_close_matches(s1[current_idx], s2)
# 			if matches:
# 				self.output += "m" + self.previous_state[current_idx]
# 				self.previous_state.remove(matches)
# 			else:
# 				self.output += "+" + self.previous_state[current_idx]
# 			self.current_state.pop(0)

# 	def handle_line_removed(self):
# 		self.output += "-" + self.previous_state.pop(0)
# 		self.current_state.pop(0)



