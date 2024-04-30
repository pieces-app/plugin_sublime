from pieces.settings import PiecesSettings
import pieces_os_client as pos_client
import sublime_plugin


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
				raise Exception
		except:
			metadata = none


		if not data:
			if selection_data.strip("\n"):
				data = selection_data
			else:
				return # No data 
		assets_api = pos_client.AssetsApi(PiecesSettings.api_client)

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
		created_asset = assets_api.assets_create_new_asset(transferables=False, seed=seed)
		self.view.window().run_command("pieces_list_assets",{"pieces_asset_id":created_asset.id})
