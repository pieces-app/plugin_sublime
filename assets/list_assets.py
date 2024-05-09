import sublime_plugin
import sublime
import mdpopups
import re

from .utils import tabulate_from_markdown,AssetSnapshot
from pieces_os_client import *
from pieces.settings import PiecesSettings




class PiecesListAssetsCommand(sublime_plugin.WindowCommand):
	sheets_md = {} # {Sheetid : {asset:property}}
	def run(self,pieces_asset_id):

		api_instance = AssetApi(PiecesSettings.api_client)
		api_response = api_instance.asset_specific_asset_export(pieces_asset_id, "MD")
		
		markdown_text = api_response.raw.string.raw

		markdown_text_table = tabulate_from_markdown(markdown_text)

		sheet = mdpopups.new_html_sheet(self.window,api_response.name,markdown_text_table,css = ".div_wrapper {margin-left:2rem}",wrapper_class="div_wrapper")
		
		
		sheet_id = sheet.id()
		code_block_pattern = r'(```[\s\S]*?\n```)'


		# Find all code blocks
		code_block = re.findall(code_block_pattern, markdown_text)
		try:
			language = AssetSnapshot.assets_snapshot[pieces_asset_id].original.reference.classification.specific
		except:
			language = None
		PiecesListAssetsCommand.sheets_md[sheet_id] = {"code":"\n".join(code_block[0].split("\n")[1:-1]),"name":api_response.name,"language":language,"id":pieces_asset_id}


	def input(self,args):
		return PiecesAssetIdInputHandler()







class PiecesAssetIdInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		assets_list = []
		for asset_id in AssetSnapshot.loaded_assets_identifiers_snapshot:
			asset = AssetSnapshot.assets_snapshot[asset_id]
			name = asset.name if asset.name else "New asset"
			try:
				appedned = False
				annotations = asset.annotations.iterable
				annotations = sorted(annotations, key=lambda x: x.updated.value, reverse=True)
				for annotation in annotations:
					if annotation.type == "DESCRIPTION":
						appedned = True
						assets_list.append(sublime.ListInputItem(text=name, value=asset_id,details=annotation.text))
						break
				if not appedned:
					raise Exception()
			except:
				assets_list.append(sublime.ListInputItem(text=name, value=asset_id))


		return assets_list

	def placeholder(self):
		return "Choose an asset"

