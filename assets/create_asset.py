from ..settings import PiecesSettings
import pieces_os_client as pos_client
import sublime_plugin
import sublime


class PiecesCreateAssetCommand(sublime_plugin.TextCommand):
	def run(self,edit,data=None):
		# Get the all the selected text
		selection_data = "\n".join([self.view.substr(selection) for selection in self.view.sel()])
		

		# Getting the metadata
		try:
			ext = self.view.file_name().split(".")[-1]

			if ext in pos_client.ClassificationSpecificEnum:
				metadata = pos_client.FragmentMetadata(ext=ext)
			else:
				raise IndexError
		except IndexError:
			metadata = none


		if not data:
			if selection_data.strip("\n"):
				data = selection_data
			else:
				return # No data 
		

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

		

		# Creating the new asset using the assets API
		sublime.set_timeout_async(lambda : self.run_create_async(self.view,seed) ,0)

		

	@staticmethod
	def run_create_async(view,seed):
		view.set_status('Pieces Creating', 'Creating an asset')
		assets_api = pos_client.AssetsApi(PiecesSettings.api_client)

		created_asset_id = assets_api.assets_create_new_asset(transferables=False, seed=seed).id
		
		view.window().run_command("pieces_list_assets",{"pieces_asset_id":created_asset_id})
		view.erase_status('Pieces Creating')


	def is_enabled(self):
		return PiecesSettings().is_loaded
