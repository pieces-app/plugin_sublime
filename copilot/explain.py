import sublime_plugin
import sublime
from .._pieces_lib.pieces_os_client import (QGPTTaskPipeline,
											QGPTTaskPipelineForCodeExplanation)
from .ask_command import copilot
from ..settings import PiecesSettings

class PiecesExplainCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		# Get the all the selected text
		data = "\n".join([self.view.substr(selection) for selection in self.view.sel()])
		if not data:
			return sublime.error_message("Please select a text")
		copilot.clear()
		ext = self.view.file_name().split(".")[-1] if self.view.file_name() else 'txt'
		query = f"Can you explain this \n```{ext}\n{data}\n```"
		copilot.render_conversation(None)
		copilot.add_query(query)
		copilot.ask(
			pipeline=QGPTTaskPipeline(
				code_explanation=QGPTTaskPipelineForCodeExplanation()
			)
		)

	def is_enabled(self):
		return PiecesSettings.is_loaded