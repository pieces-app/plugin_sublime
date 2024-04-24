import sublime_plugin
import sublime
import mdpopups
import re
from typing import Dict

from pieces_os_client import *
from pieces import config





assets_identifiers_snapshot = []

# saved_code_blocks = {}

sheets_md = {}


class PiecesListAssetsCommand(sublime_plugin.WindowCommand):
	max_assets = 10
	sheets_md = {}
	def run(self,pieces_asset_id):
		if pieces_asset_id == "LOAD":
			PiecesListAssetsCommand.max_assets += 10
			return self.window.run_command("pieces_list_assets")


		api_instance = AssetApi(config.api_client)
		api_response = api_instance.asset_specific_asset_export(pieces_asset_id, "MD")
		
		markdown_text = api_response.raw.string.raw

		markdown_text_table = tabulate_from_markdown(markdown_text)

		sheet = mdpopups.new_html_sheet(self.window,api_response.name,markdown_text_table,css = ".div_wrapper {margin-left:2rem}",wrapper_class="div_wrapper")
		
		
		sheet_id = sheet.id()
		code_block_pattern = r'(```[\s\S]*?\n```)'


		# Find all code blocks
		code_block = re.findall(code_block_pattern, markdown_text)
		try:
			iterable = AssetSnapshot.assets_snapshot[pieces_asset_id].formats.iterable
			sorted_iterable = sorted(iterable, key=lambda x: x.updated.value, reverse=True)
			language = sorted_iterable[0].analysis.code.language
		except:
			language = None
		PiecesListAssetsCommand.sheets_md[sheet_id] = {"code":"\n".join(code_block[0].split("\n")[1:-1]),"name":api_response.name,"language":language,"id":pieces_asset_id}

		# Add "Copy this Python code:" before each code block
		# for idx,block in enumerate(code_blocks):
		# 	code_block_id = f'{sheet_id}/{idx}'
		# 	saved_code_blocks[code_block_id] = block
		# 	{"id":f"{code_block_id}","action":"copy"}
		# 	url = sublime.command_url("pieces_add_code")
		# 	div = f'<div style="display:inline-block;"><a href="{url}">copy</a></div>\n'
		# 	markdown_text = markdown_text.replace(block,div + block)

		# return mdpopups.update_html_sheet(sheet,markdown_text)

	def input(self,args):
		return PiecesAssetIdInputHandler()






class PiecesHandleMarkdownCommand(sublime_plugin.WindowCommand):
	views_to_handler = {}
	def run(self,mode):
		sheet = self.window.active_sheet()
		sheet_details = None
		if sheet:
			sheet_details = PiecesListAssetsCommand.sheets_md.get(sheet.id())
		
		if mode == "save":
			self.handle_save()
		
		if not sheet_details:
			if mode == "copy":
				self.window.run_command("copy")
			return
			
		self.code = sheet_details["code"]
		self.language = sheet_details["language"]
		self.name = sheet_details["name"]
		self.asset_id = sheet_details["id"]

		if mode == "copy":
			self.handle_copy()
		elif mode == "edit":
			self.handle_edit()



	def handle_save(self):
		view = self.window.active_view()
		if view:
			asset_id = PiecesHandleMarkdownCommand.views_to_handler.get(view.id())
			if asset_id:
				asset = AssetSnapshot.get_asset_snapshot(asset_id)
				format_api = FormatApi(config.api_client)
				original = format_api.format_snapshot(asset.original.id, transferable=True)
				if original.classification.generic == ClassificationGenericEnum.IMAGE:
					sublime.error_message("Could not edit an image")
					return
				data = view.substr(sublime.Region(0, view.size()))
				if original.fragment.string.raw:
					original.fragment.string.raw = data
				elif original.file.string.raw:
					original.file.string.raw = data
				format_api.format_update_value(transferable=False, format=original)
				PiecesListAssetsCommand().run(pieces_asset_id=asset_id)
				view.close()
			else:
				self.window.run_command("save")

	def handle_copy(self):
		sublime.set_clipboard(self.code)
	def handle_edit(self):
		# Create a new file
		view = self.window.new_file(syntax = f'Packages/{self.language}/{self.language}.sublime-syntax')
		# Insert the text
		view.run_command('insert', {'characters': self.code})
		# Set the name
		view.set_name(self.name)
		# Set it to avoid the saving dialog 
		view.set_scratch(True)
		# Set the view to handle the save operation
		PiecesHandleMarkdownCommand.views_to_handler[view.id()] = self.asset_id





class PiecesAssetIdInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		global assets_identifiers_snapshot
		assets_list = []
		for asset_id in assets_identifiers_snapshot[:PiecesListAssetsCommand.max_assets]:
			asset = AssetSnapshot.get_asset_snapshot(asset_id)
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


		assets_list.append(sublime.ListInputItem(text="Load more assets", value="LOAD",details="load 10 more assets"))
		return assets_list

	def placeholder(self):
		return "Choose an asset"




def assets_snapshot_callback(ids_json):
	global assets_identifiers_snapshot

	assets_identifiers_snapshot.extend([item['asset']['id'] for item in ids_json.get('iterable',[])])

    # Return the list of ids
	return assets_identifiers_snapshot



class AssetSnapshot():
	assets_snapshot:Dict[str,Asset] = {}
	@classmethod
	def get_asset_snapshot(cls,id):
		if id not in cls.assets_snapshot.keys():
			api_instance = AssetApi(config.api_client)
			asset = api_instance.asset_snapshot(id)
			cls.assets_snapshot[id] = asset
			return asset
		else:
			return cls.assets_snapshot[id]







def tabulate_from_markdown(md_text):
	# Split the markdown text into lines
	lines = md_text.split('\n')

	# Filter out lines that contain '|', and join them back into a string
	table_md = "\n".join(line for line in lines if '|' in line)

	# Split the markdown table into lines, and then into cells
	# Also, remove leading/trailing whitespace from each cell
	data = [[cell.strip() for cell in line.split("|")[1:-1]] for line in table_md.strip().split("\n")]

	headers = "<div>"
	for header in data[0]:
		if header:
			headers += "<span><h1>" + header + "</h1></span>"

    # Generate HTML string
	html_text = f"{headers}</div><br><div>"
	for row in data[2:]:
		html_text += "<div>"
		for idx,cell in enumerate(row):
			if idx == 0:
				cell += ": " 
			html_text += "<span>" + cell + "</span>"
		html_text += "<br><br></div>"
	html_text += "</div>"


	return md_text.replace(table_md,html_text)