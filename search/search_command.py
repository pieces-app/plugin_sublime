import sublime_plugin
import sublime

from pieces.settings import PiecesSettings
from pieces.assets.utils import AssetSnapshot
from pieces.assets.list_assets import PiecesAssetIdInputHandler

from pieces_os_client import SearchApi,AssetsApi




class QueryInputHandler(sublime_plugin.TextInputHandler):
	def placeholder(self):
		return "Enter a quick description of the bug itself or useful error message"

	def validate(self, text):
		return len(text) > 0

	def placeholder(self):
		return "Enter a query"

	def preview(self,text):
		result = PiecesSearchCommand.search(SearchTypeInputHandler.search_type,query = text)
		if result:
			names_html = [f"<li>{asset.name}</li>" for id,asset in result.items()]
			return sublime.Html(f"""<p>Asset Matches:</p><ul>{"".join(names_html)}</ul>""")

	def next_input(self,args):
		result = PiecesSearchCommand.search(**args)

		if not result: # No results just set the status
			sublime.active_window().active_view().set_status('Pieces Search', 'No matches found.')
			return

		return PiecesAssetIdExtendInputHandler(result) # get a choose menu of the assets found



class SearchTypeInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		return [
			("Neural Code Search","ncs"),
			("Full Text Search", "fts"),
			("Fuzzy Search", "assets")
		]
	def next_input(self,args):
		SearchTypeInputHandler.search_type = args["search_type"] # used in the preview
		return QueryInputHandler()
	def placeholder(self):
		return "Choose the type of searching."

class PiecesSearchCommand(sublime_plugin.WindowCommand):
	asset_api = AssetsApi(PiecesSettings.api_client)
	search_api = SearchApi(PiecesSettings.api_client)

	def run(self,search_type,query,pieces_asset_id=None):
		return self.window.run_command("pieces_list_assets",args={"pieces_asset_id":pieces_asset_id})

	@staticmethod
	def search(search_type,query)-> list:
		if search_type == 'assets':
			results = PiecesSearchCommand.asset_api.assets_search_assets(query=query, transferables=False)
		elif search_type == 'ncs':
			results = PiecesSearchCommand.search_api.neural_code_search(query=query)
		elif search_type == 'fts':
			results = PiecesSearchCommand.search_api.full_text_search(query=query)
			# Check and extract asset IDs from the results
		if results:
			# Extract the iterable which contains the search results
			iterable_list = results.iterable if hasattr(results, 'iterable') else []

			# Check if iterable_list is a list and contains SearchedAsset objects
			if isinstance(iterable_list, list) and all(hasattr(asset, 'exact') and hasattr(asset, 'identifier') for asset in iterable_list):
				# Extracting suggested and exact IDs
				suggested_ids = [asset.identifier for asset in iterable_list if not asset.exact]
				exact_ids = [asset.identifier for asset in iterable_list if asset.exact]

				# Combine and store best and suggested matches in asset_ids
				combined_ids = exact_ids + suggested_ids

				# Print the combined asset details
				if combined_ids:
					return {id:AssetSnapshot.assets_snapshot.get(id) for id in combined_ids if AssetSnapshot.assets_snapshot.get(id)}


	def input(self,args):
		return SearchTypeInputHandler()



class PiecesAssetIdExtendInputHandler(PiecesAssetIdInputHandler):
	def __init__(self,results):
		self.results = results
		
	def name(self):
		return "pieces_asset_id"

	def list_items(self):
		return self.get_assets_list(self.results)

