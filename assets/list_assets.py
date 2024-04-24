import sublime_plugin
import sublime

from pieces_os_client import *
from pieces import config

from . import assets_identifiers_ws

max_assets = 10


assets_snapshot = {}
assets_identifiers_snapshot = []

class PiecesListAssetsCommand(sublime_plugin.WindowCommand):
	
	def run(self,pieces_asset_id):
		if pieces_asset_id == "LOAD":
			global max_assets
			max_assets += 10
			return self.window.run_command("pieces_list_assets")
		print(pieces_asset_id)

	def input(self,args):
		return PiecesAssetIdInputHandler()


class PiecesAssetIdInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		global max_assets,assets_identifiers_snapshot
		assets_list = []
		for asset_id in assets_identifiers_snapshot[:max_assets]:
			asset = get_asset_snapshot(asset_id)
			name = asset.get("name","New asset")
			assets_list.append(sublime.ListInputItem(text=name, value=asset_id))


		assets_list.append(sublime.ListInputItem(text="Load more assets", value="LOAD",details="load 10 more assets"))
		return assets_list

	def placeholder(self):
		return "Choose an asset"





def assets_snapshot_callback(ids_json):
	global assets_identifiers_snapshot

	assets_identifiers_snapshot.extend([item['asset']['id'] for item in ids_json.get('iterable',[])])



    # Return the list of ids
	return assets_identifiers_snapshot




def get_asset_snapshot(id):
	global assets_snapshot
	if id not in assets_snapshot.keys():
		api_instance = AssetApi(config.api_client)
		asset = api_instance.asset_snapshot(id).to_dict()
		assets_snapshot[id] = asset
		return asset
	else:
		return assets_snapshot[id]