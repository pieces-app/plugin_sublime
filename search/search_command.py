import sublime_plugin
import sublime
from typing import List, Optional

from ..startup_utils import check_pieces_os
from ..assets.list_assets import PiecesAssetIdInputHandler

from .._pieces_lib.pieces_os_client.wrapper.basic_identifier import BasicAsset



class QueryInputHandler(sublime_plugin.TextInputHandler):
	def placeholder(self):
		return "Enter a search query"

	def validate(self, text):
		return len(text) > 0

	def placeholder(self):
		return "Enter a query"

	def preview(self,text):
		if not text:
			return
		result = PiecesSearchCommand.search(SearchTypeInputHandler.search_type,query = text)
		if result:
			names_html = []
			for asset in result:
				try:
					names_html.append(f"<li>{asset.name}</li>")
				except ValueError: # Asset id is not valid
					pass
			return sublime.Html(f"""<p>Asset Matches:</p><ul>{"".join(names_html)}</ul>""")

	def next_input(self,args):
		result = PiecesSearchCommand.search(**args)

		if not result: # No results just set the status
			sublime.status_message('No matches found.')

		return PiecesAssetIdExtendInputHandler(result) # get a choose menu of the assets found



class SearchTypeInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		return [
			("Neural Code Search","ncs"),
			("Full Text Search", "fts"),
			("Fuzzy Search", "fuzzy")
		]
	def next_input(self,args):
		SearchTypeInputHandler.search_type = args["search_type"] # used in the preview
		return QueryInputHandler()
	def placeholder(self):
		return "Choose the type of searching."

class PiecesSearchCommand(sublime_plugin.WindowCommand):
	@check_pieces_os()
	def run(self,search_type,query,pieces_asset_id=None):
		if pieces_asset_id:
			return self.window.run_command("pieces_list_assets",args={"pieces_asset_id":pieces_asset_id})

	@staticmethod
	def search(search_type,query)-> Optional[List[BasicAsset]]:
		return BasicAsset.search(query,search_type)

	@check_pieces_os(True)
	def input(self,args):
		return SearchTypeInputHandler()



class PiecesAssetIdExtendInputHandler(PiecesAssetIdInputHandler):
	def __init__(self,results):
		self.results = results
		
	def name(self):
		return "pieces_asset_id"

	def list_items(self):
		return self.get_assets_list(self.results)

