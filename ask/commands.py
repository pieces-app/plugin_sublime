import sublime
import sublime_plugin
import pieces_os_client as pos_client
from pieces.settings import PiecesSettings
import re
import difflib


bugs_prompt = """Act as a programmer to fix this bug
There is a bug in this codebase fix it provided to you
Here is a quick description: {description}
Here is the code {code}"""
LIST_ITEMS = [
	("Check for bugs",bugs_prompt)
]


class DescriptionInputHandler(sublime_plugin.TextInputHandler):
	def placeholder(self):
		return "Enter a quick description of the bug itself or useful error message"


class QuestionInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		return LIST_ITEMS
	def next_input(self,args):
		return DescriptionInputHandler()




class PiecesAskQuestionCommand(sublime_plugin.TextCommand):
	def run(self,edit, question, description):
		# Get the current selection
		self.selection = self.view.sel()[0]
		selected_text = self.view.substr(self.selection)

		if not selected_text:
			return # TODO show error
		
		res = pos_client.QGPTApi(PiecesSettings.api_client).question(
			pos_client.QGPTQuestionInput(
				query = question.format(description=description,code=selected_text),
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
		self.window  = self.view.window()
		response_code = res.answers.iterable[0].text
		
		# Regular expression pattern for code block
		pattern = r'```.*?\n(.*?)```'

		# Find all matches in the markdown text
		match = re.search(pattern, response_code, re.DOTALL)
		if match:
			self.code = match.group(1)
			self.code_html = get_differences(self.view,selected_text.splitlines(),self.code.splitlines())
			link = "<a href=insert>Insert the code</a>"
			html = f"<div style='display:inline-block'>{link}</div>{self.code_html}"

			# Calculate the length of the code_html
			code_html_length = len(self.code_html)

			# Create a phantom at the end of the current selection
			phantom_region = sublime.Region(self.selection.end(), self.selection.end() + code_html_length)
			self.phantom = mdpopups.add_phantom(self.view,"code_phantom", phantom_region, html, sublime.LAYOUT_INLINE,md=False,on_navigate=self.on_nav)
			print(self.phantom)


	def on_nav(self, href):
		if href == "insert":
			# Replace the selected text with the code
			self.view.run_command("replace_selection", {"code": self.code, "selection": [self.selection.a, self.selection.b]})
			# Remove the phantom
			mdpopups.erase_phantoms("code_phantom")

			
	def input(self,args):
		return QuestionInputHandler()




def get_differences(view,s1:list,s2:list):
	# Create a Differ object
	differ = difflib

    # Compare the snippets
	diffs = differ.unified_diff(s1, s2)

	for diff in diffs:
		if diff.startswith("+"):
			print(mdpopups.md2html(view,f"```python{diff[1:]}```"))
			final_output += '<span style="background-color:green">' + diff + '</span>'
		elif diff.startswith("-"):
			print(mdpopups.md2html(view,f"```python{diff[1:]}```"))
			final_output += '<span style="background-color:red">' + diff + '</span>'
		elif diff.startswith("?"):
			continue
		final_output += "<br>"


	return final_output


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



