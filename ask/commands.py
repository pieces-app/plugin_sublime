import sublime
import sublime_plugin
import textwrap
from .._pieces_lib.pieces_os_client import (
	QGPTTaskPipelineForCodeFix,
	QGPTTaskPipeline,
	QGPTTaskPipelineForCodeCommentation,
	QGPTTaskPipelineForCodeModification,
	QGPTApi,
	Seed,
	SeededFormat,
	SeededAsset,
	SeededFragment,
	RelevantQGPTSeed,
	QGPTPromptPipeline,
	RelevantQGPTSeeds,
	TransferableString,
	QGPTQuestionInput,
	ClassificationSpecificEnum,
	SeededClassification)
import re
import mdpopups

from .diff import show_diff_popup
from ..settings import PiecesSettings

from ..startup_utils import check_pieces_os

description_needed_commands = {
	"modify":"Enter the instructions that should we use to modify that code",
	"fix":"Enter the error message that you got"
}

class PiecesAskQuestionCommand(sublime_plugin.TextCommand):
	@check_pieces_os()
	def run(self,edit, task):
		# task = comment,fix,modify
		self.task = task
		sublime.set_timeout_async(self.run_async,0)


	def run_async(self):
		# Get the current selection
		self.selection = self.view.sel()[0]
		# Modify the selection to whole line not part of it 
		self.selection = sublime.Region(self.view.line(self.selection.begin()).begin(),self.selection.end()) 
		self.selected_text = textwrap.dedent(self.view.substr(self.selection))

		# Getting the langauge
		try:
			ext = self.view.file_name().split(".")[-1]

			if ext in ClassificationSpecificEnum:
				self.classification = SeededClassification(specific = ext)
			else:
				raise AttributeError
		except:
			self.classification = None

		if not self.selected_text:
			sublime.error_message("Please select a text to ask about!")
			return 

		description_placeholder = description_needed_commands.get(self.task)
		
		if description_placeholder:
			sublime.active_window().show_input_panel(description_placeholder, "", self.on_done, None, None)
		else:
			self.on_done_async()



	def on_done(self,description):
		self._description = description
		if not description:
			description = "No description provided"
		sublime.set_timeout_async(self.on_done_async,0)

	def on_done_async(self):
		if self.task == "fix":
			task = QGPTTaskPipeline(code_fix=QGPTTaskPipelineForCodeFix(error=self._description))
		elif self.task == "modify":
			task = QGPTTaskPipeline(code_modification=QGPTTaskPipelineForCodeModification(instruction=self._description))
		else: # comment
			task = QGPTTaskPipeline(code_commentation=QGPTTaskPipelineForCodeCommentation())
		
		self.view.set_status('Pieces Refactoring', 'Copilot is thinking...')

		relevant = RelevantQGPTSeeds(
			iterable = [
				RelevantQGPTSeed(
					seed = Seed(
						type="SEEDED_ASSET",
						asset=SeededAsset(
							application=PiecesSettings.api_client.tracked_application,
							format=SeededFormat(
								fragment = SeededFragment(
									string = TransferableString(raw = self.selected_text)
								),
								classification = self.classification
							),
						), 
					),
				)
			]
		)
		pipeline = QGPTPromptPipeline(task=task)
		try:
			res = PiecesSettings.api_client.copilot.question(" ",relevant,pipeline)
		except:
			self.view.set_status('Pieces Refactoring', 'Copilot error in getting the responses')
			sublime.set_timeout(lambda:self.view.erase_status("Pieces Refactoring"),5000)
			return
		self.view.set_status('Pieces Refactoring', 'Copilot analyzing...')
		self.window  = self.view.window()

		response_code = res.answers.iterable[0].text
		
		# Regular expression pattern for code block
		pattern = r'```.*?\n(.*?)```'

		# Find all matches in the markdown text
		match = re.search(pattern, response_code, re.DOTALL)
		if match:
			self.code = match.group(1)
			self.selected_text = self.selected_text.replace("\t","    ")
			show_diff_popup(self.view, self.selected_text.splitlines(), self.code.splitlines(),
				on_nav=self.on_nav,region=sublime.Region(self.selection.a,self.selection.b))
			
			self.is_done = True
		else:
			mdpopups.show_popup(self.view,response_code,md=True) # No code found
		self.view.erase_status('Pieces Refactoring')


	def on_nav(self, href):
		if href == "insert":
			# Replace the selected text with the code
			self.view.run_command("pieces_replace_code_selection", {"code": self.code, "selection": [self.selection.a, self.selection.b]})
			# Remove the popup
			self.view.erase_phantoms("pieces_ask")
		elif href == "dismiss":
			self.view.erase_phantoms("pieces_ask")




class PiecesReplaceCodeSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit, code, selection):
		# Convert the selection into a Region
		region = sublime.Region(selection[0], selection[1])

		# Retrieve the settings for tabs vs. spaces and the number of spaces per tab
		settings = self.view.settings()
		use_spaces = settings.get('translate_tabs_to_spaces')
		tab_size = settings.get('tab_size', 4)


		# Get the current indentation level of the selected region
		current_line_region = self.view.line(region.begin())
		current_line_text = self.view.substr(current_line_region)
		current_indentation = self._get_indentation(current_line_text, tab_size)

		# Adjust the indentation of the replacement code
		indented_code = self._adjust_indentation(code, current_indentation, use_spaces, tab_size)

		# Replace the current selection with the indented code
		self.view.replace(edit, region, indented_code)

	def _get_indentation(self, line_text, tab_size):
		"""Calculate the indentation level of the given line."""
		indentation = 0
		for char in line_text:
			if char == '\t':
				indentation += tab_size
			elif char == ' ':
				indentation += 1
			else:
				break
		return indentation

	def _adjust_indentation(self, code, indentation, use_spaces, tab_size):
		"""Adjust the indentation of the given code."""
		lines = code.split('\n')
		indent_char = ' ' * tab_size if use_spaces else '\t'
		indent_string = indent_char * (indentation // tab_size) + ' ' * (indentation % tab_size)
		indented_lines = [indent_string + line if line.strip() else line for line in lines]
		return '\n'.join(indented_lines)

