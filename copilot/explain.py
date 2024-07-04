import sublime_plugin
import sublime
from .._pieces_lib.pieces_os_client import (QGPTTaskPipeline,
											QGPTTaskPipelineForCodeExplanation,
											RelevantQGPTSeed,
											RelevantQGPTSeeds,
											)
from .ask_command import copilot
from ..assets.create_asset import PiecesCreateAssetCommand

class PiecesExplainCommand(sublime_plugin.TextCommand):
	def run(self,edit):
		copilot.clear()
		ext = self.view.file_name().split(".")[-1]
		seed = PiecesCreateAssetCommand(self.view).get_seeds()
		query = f"Can you explain this \n```{ext}\n{seed.asset.format.fragment.string.raw}\n```"
		copilot.add_query(query)
		copilot.ask(
			relevant=RelevantQGPTSeeds(
				iterable=[RelevantQGPTSeed(seed=seed)]
			),
			pipeline=QGPTTaskPipeline(
				code_explanation=QGPTTaskPipelineForCodeExplanation()
				)
		)

