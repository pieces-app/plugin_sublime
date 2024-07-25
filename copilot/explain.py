import sublime_plugin
from .._pieces_lib.pieces_os_client import (QGPTTaskPipeline,
											QGPTTaskPipelineForCodeExplanation)
from .ask_command import copilot
from ..assets.create_asset import PiecesCreateAssetCommand
from ..settings import PiecesSettings

class PiecesExplainCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		copilot.clear()
		if self.view.file_name():
			ext = self.view.file_name().split(".")[-1]
		else: ext = 'txt'
		seed = PiecesCreateAssetCommand(self.view).get_seeds()
		query = f"Can you explain this \n```{ext}\n{seed.asset.format.fragment.string.raw}\n```"
		copilot.add_query(query)
		# copilot.add_context(seed=seed)
		copilot.ask(
			pipeline=QGPTTaskPipeline(
				code_explanation=QGPTTaskPipelineForCodeExplanation()
				)
		)

	def is_enabled(self):
		return PiecesSettings().is_loaded