import sublime_plugin
import sublime
import mdpopups
import re
from typing import List

from .._pieces_lib.pieces_os_client.wrapper.websockets import AssetsIdentifiersWS
from .._pieces_lib.pieces_os_client.wrapper.basic_identifier import BasicAsset
from .._pieces_lib.pieces_os_client import *
from ..settings import PiecesSettings
from ..startup_utils import check_pieces_os

A_TAG_STYLE = "padding:2px 5px; background-color: var(--accent); border-radius: 6px;color: var(--foreground);text-align:center;text-decoration: None;display:inline"

HTML_CODE_BUTTON_CONTENT = '<div style="margin-top:2px">{content}</div>'

class PiecesListAssetsCommand(sublime_plugin.WindowCommand):
	sheets_md = {} # {Sheetid : asset_id}
	shareable_link = [] # asset_ids

	@check_pieces_os()
	def run(self,pieces_asset_id):
		self.pieces_asset_id = pieces_asset_id
		sublime.set_timeout_async(self.run_async,0)

	def run_async(self):
		self.sheet = self.window.new_html_sheet("Loading","")
		self.sheet_id = self.sheet.id()
		self.update_sheet(self.sheet,self.pieces_asset_id, {})


	@classmethod
	def update_sheet(cls,sheet,asset_id,buttons_kwargs={}):
		asset = BasicAsset(asset_id)
		try:
			markdown_text = asset.markdown
		except:
			return sublime.error_message("Asset Not Found")
		if (not buttons_kwargs.get("share")) and (asset.shares):
			buttons_kwargs["share"] = {
				"title":"Copy Generated Link",
				"url":f'subl:pieces_copy_link  {{"content":"{asset.shares[0].link}", "asset_id":"{asset_id}"}}'}

		markdown_text_table = tabulate_from_markdown(markdown_text,buttons = cls.create_html_buttons(sheet.id(),**buttons_kwargs))
		
		mdpopups.update_html_sheet(sheet,markdown_text_table,css = ".div_wrapper {margin-left:2rem}",wrapper_class="div_wrapper")

		
		try:
			sheet.set_name(asset.name)
		except:
			pass
		cls.sheets_md[sheet.id()] = asset_id

	
	@classmethod
	def create_html_buttons(cls,sheet_id,**kwargs):
		"""
			Sheet ID: which these buttons gonna be generated
			kwargs: Overwrite the buttons title and url
			{button_name:{url:,title:}}
		"""

		content = ''
		for button in ["copy","edit","share","delete"]:
			button_details = kwargs.get(button,{})
			href = button_details.get("url")
			if not href:
				href = f'subl:pieces_handle_markdown {{"sheet_id":"{sheet_id}","mode":"{button}"}}'
			content += f"""<a style="{A_TAG_STYLE}" href='{href}'>{button_details.get("title",button.title())}</a>&nbsp;"""
	
		return HTML_CODE_BUTTON_CONTENT.format(content=content)

	@check_pieces_os(True)
	def input(self,args):
		return PiecesAssetIdInputHandler()


class PiecesAssetIdInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		return self.get_assets_list(PiecesSettings.api_client.assets())

	def get_assets_list(self,assets_snapshot:List[BasicAsset]):
		assets_list = []
		for basic_asset in assets_snapshot:
			name = basic_asset.name
			annotation = basic_asset.description
			if annotation:
				assets_list.append(sublime.ListInputItem(text=name, value=basic_asset.id,details=annotation))
			else:
				assets_list.append(sublime.ListInputItem(text=name, value=basic_asset.id))
		return assets_list

	def placeholder(self):
		return "Choose an asset"


def tabulate_from_markdown(md_text,buttons):
	table_regex = re.compile(r'(\|.*\|(?:\n\|.*\|)+)')
	match = table_regex.search(md_text)

	if match:
		table_md = match.group(1)
	else: return md_text

	# Split the markdown table into lines, and then into cells
	# Also, remove leading/trailing whitespace from each cell
	data = [[cell.strip() for cell in line.split("|")[1:-1]] for line in table_md.strip().split("\n")]

    # Generate HTML string
	html_text = f"<div style='margin-bottom:13px'>{buttons}</div><h3>{data[0][0]}</h3><br><div>"
	for row in data[2:]:
		html_text += "<div>"
		for idx,cell in enumerate(row):
			if idx == 0:
				cell += ": " 
			html_text += "<span>" + cell + "</span>"
		html_text += "<br><br></div>"
	html_text += "</div>"


	return md_text.replace(table_md,html_text)