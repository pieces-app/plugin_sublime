from ..settings import PiecesSettings
from ..startup_utils import check_pieces_os
from .._pieces_lib.pieces_os_client import ClassificationSpecificEnum,FragmentMetadata
import sublime_plugin
import sublime


class PiecesCreateAssetCommand(sublime_plugin.TextCommand):
	@check_pieces_os()
	def run(self,edit,data=None,metadata=None):
		if not data:
			# Get the all the selected text
			data = "\n".join([self.view.substr(selection) for selection in self.view.sel()])
			if not data:
				return sublime.error_message("Please select a text")
			ext = self.view.name().split(".")[-1]
			metadata = FragmentMetadata(ext = ClassificationSpecificEnum(ext)) if ext in ClassificationSpecificEnum else None
		
		# Creating the new asset using the assets API
		sublime.set_timeout_async(lambda :self.run_create_async(data,metadata) ,0)

	
	def run_create_async(self,data,metadata):
		self.view.set_status('Pieces Creating', 'Creating an asset')
		created_asset_id = PiecesSettings.api_client.create_asset(data,metadata)
		self.view.window().run_command("pieces_list_assets",{"pieces_asset_id":created_asset_id})
		self.view.erase_status('Pieces Creating')

