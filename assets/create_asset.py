from ..settings import PiecesSettings
from .._pieces_lib import pieces_os_client as pos_client
import sublime_plugin
import sublime


class PiecesCreateAssetCommand(sublime_plugin.TextCommand):

	def get_seeds(self,data=None):

		if not data:
			# Get the all the selected text
			data = "\n".join([self.view.substr(selection) for selection in self.view.sel()])
			if not data:
				return sublime.error_message("Please select a text")


		# Getting the metadata
		if not data:
			try:
				ext = self.view.file_name().split(".")[-1]

				if ext in pos_client.ClassificationSpecificEnum:
					metadata = pos_client.FragmentMetadata(ext=ext)
				else:
					raise IndexError
			except:
				metadata = None
		else:
			metadata = None
		
		

		# Construct a Seed
		seed = pos_client.Seed(
			asset=pos_client.SeededAsset(
				application=PiecesSettings.get_application(),
					format=pos_client.SeededFormat(
							fragment=pos_client.SeededFragment(
								string=pos_client.TransferableString(raw=data),
								metadata=metadata
							)
						),
					metadata=None
				),
			type="SEEDED_ASSET"
		)
		return seed
	def run(self,edit,data=None):
		seed = self.get_seeds(data)
		
		# Creating the new asset using the assets API
		sublime.set_timeout_async(lambda : self.run_create_async(seed) ,0)

		

	
	def run_create_async(self,seed):
		self.view.set_status('Pieces Creating', 'Creating an asset')
		created_asset_id = self.create_asset(seed)
		self.view.window().run_command("pieces_list_assets",{"pieces_asset_id":created_asset_id})
		self.view.erase_status('Pieces Creating')
	
	@staticmethod
	def create_asset(seed):
		assets_api = pos_client.AssetsApi(PiecesSettings.api_client)
		created_asset_id = assets_api.assets_create_new_asset(transferables=False, seed=seed).id
		return created_asset_id


	def is_enabled(self):
		return PiecesSettings().is_loaded
