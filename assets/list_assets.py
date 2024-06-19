import sublime_plugin
import sublime
import mdpopups
import re

from .utils import tabulate_from_markdown,AssetSnapshot
from pieces_os_client import *
from ..settings import PiecesSettings


A_TAG_STYLE = "padding:2px 5px; background-color: var(--accent); border-radius: 6px;color: var(--foreground);text-align:center;text-decoration: None;display:inline"

HTML_CODE_BUTTON_CONTENT = '<div style="margin-top:2px">{content}</div>'

class PiecesListAssetsCommand(sublime_plugin.WindowCommand):
	sheets_md = {} # {Sheetid : {code,name,langauge,id}}
	shareable_link = [] # asset_ids
	def run(self,pieces_asset_id):
		if not pieces_asset_id in AssetSnapshot.assets_snapshot:
			return
		self.pieces_asset_id = pieces_asset_id
		sublime.set_timeout_async(self.run_async,0)

	def run_async(self):
		self.sheet = self.window.new_html_sheet("Loading","")
		self.sheet_id = self.sheet.id()
		self.update_sheet(self.sheet,self.pieces_asset_id)
		


	@classmethod
	def update_sheet(cls,sheet,asset_id,buttons_kwargs={}):
		api_instance = AssetApi(PiecesSettings.api_client)
		api_response = api_instance.asset_specific_asset_export(asset_id, "MD")
		
		
		markdown_text = api_response.raw.string.raw

		
		code_block_pattern = r'(```[\s\S]*?\n```)'

		# Find all code blocks
		code_block = re.findall(code_block_pattern, markdown_text)[0]
		
		markdown_text_table = tabulate_from_markdown(markdown_text,buttons = cls.create_html_buttons(asset_id,sheet.id(),**buttons_kwargs))
		
		mdpopups.update_html_sheet(sheet,markdown_text_table,css = ".div_wrapper {margin-left:2rem}",wrapper_class="div_wrapper")

		
		try:
			sheet.set_name(api_response.name)
		except:
			pass
		try:
			language = AssetSnapshot.assets_snapshot[asset_id].original.reference.classification.specific
		except:
			language = None
		cls.sheets_md[sheet.id()] = {"code":"\n".join(code_block.splitlines()[1:-1]),"name":api_response.name,"language":language,"id":asset_id}

	
	@classmethod
	def create_html_buttons(cls,asset_id,sheet_id,**kwargs):
		content = ''
		for button in ["copy","edit","share","delete"]:
			href = ""
			if not (button == "share" and asset_id in cls.shareable_link):
				href = f'subl:pieces_handle_markdown {{"sheet_id":"{sheet_id}","mode":"{button}"}}'
			else:
				kwargs["share"] = "Sharing"
			
			content += f"""<a style="{A_TAG_STYLE}" href='{href}'>{kwargs.get(button,button.title())}</a>&nbsp;"""
		sublime.set_clipboard(HTML_CODE_BUTTON_CONTENT.format(content=content))
		return HTML_CODE_BUTTON_CONTENT.format(content=content)

	def input(self,args):
		return PiecesAssetIdInputHandler()

	def is_enabled(self):
		return PiecesSettings().is_loaded





class PiecesAssetIdInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		return self.get_assets_list(AssetSnapshot.assets_snapshot)

	def get_assets_list(self,assets_snapshot):
		assets_list = []
		for asset_id in assets_snapshot.keys():
			asset = assets_snapshot[asset_id]
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

