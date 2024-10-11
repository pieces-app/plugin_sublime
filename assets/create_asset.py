from .._pieces_lib.pieces_os_client.wrapper.basic_identifier import BasicTag,BasicAsset
from ..settings import PiecesSettings
from ..startup_utils import check_pieces_os
from .._pieces_lib.pieces_os_client import ClassificationSpecificEnum,FragmentMetadata
import sublime_plugin
import sublime
from .ext_map import file_map

class PiecesCreateAssetCommand(sublime_plugin.TextCommand):
	@check_pieces_os()
	def run(self,edit,data=None,metadata=None, add_metadata=True, open_on_save = True, tags = [], run_async = True):
		if not data:
			# Get the all the selected text
			data = "\n".join([self.view.substr(selection) for selection in self.view.sel()])
			if not data:
				return sublime.error_message("Please select a text")
			
			syntax = self.view.syntax()
			if syntax and add_metadata:
				ext = file_map.reverse.get(syntax.path)
				metadata = FragmentMetadata(ext = ClassificationSpecificEnum(ext)) if ext in ClassificationSpecificEnum else None
		

		def run_create_async():
			self.view.set_status('Pieces Creating', 'Creating an asset')
			created_asset_id = PiecesSettings.api_client.create_asset(data,metadata)
			if open_on_save:
				sublime.active_window().run_command("pieces_list_assets",{"pieces_asset_id":created_asset_id})
				self.view.erase_status('Pieces Creating')
			asset = BasicAsset(created_asset_id)

			for tag in tags:
				BasicTag.from_raw_content(PiecesSettings.api_client,tag).associate_asset(asset)
		if run_async:
			# Creating the new asset using the assets API
			sublime.set_timeout_async(run_create_async ,0)
		else:
			run_create_async()

	
	

