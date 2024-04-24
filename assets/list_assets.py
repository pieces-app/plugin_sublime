import sublime_plugin
import sublime
import mdpopups
import re

from pieces_os_client import *
from pieces import config

from . import assets_identifiers_ws

max_assets = 10


assets_snapshot = {}
assets_identifiers_snapshot = []

saved_code_blocks = {}

class PiecesListAssetsCommand(sublime_plugin.WindowCommand):
	
	def run(self,pieces_asset_id):
		if pieces_asset_id == "LOAD":
			global max_assets
			max_assets += 10
			return self.window.run_command("pieces_list_assets")

		
		api_instance = AssetApi(config.api_client)
		api_response = api_instance.asset_specific_asset_export(pieces_asset_id, "MD")
		
		markdown_text = api_response.raw.string.raw

		markdown_text = tabulate_from_markdown(markdown_text)

		sheet = mdpopups.new_html_sheet(self.window,api_response.name,markdown_text)
		
		# global saved_code_blocks
		# sheet_id = sheet.id()
		# code_block_pattern = r'(```[\s\S]*?\n```)'


		# # Find all code blocks
		# code_blocks = re.findall(code_block_pattern, markdown_text)

		# Add "Copy this Python code:" before each code block
		# for idx,block in enumerate(code_blocks):
		# 	code_block_id = f'{sheet_id}/{idx}'
		# 	saved_code_blocks[code_block_id] = block
		# 	{"id":f"{code_block_id}","action":"copy"}
		# 	url = sublime.command_url("pieces_add_code")
		# 	div = f'<div style="display:inline-block;"><a href="{url}">copy</a></div>\n'
		# 	markdown_text = markdown_text.replace(block,div + block)

		# return mdpopups.update_html_sheet(sheet,markdown_text,css = ".div_wrapper {margin-left:2rem}",wrapper_class="div_wrapper")

	def input(self,args):
		return PiecesAssetIdInputHandler()

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

    print(headers)
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

# class PiecesAddCodeCommand(sublime_plugin.WindowCommand):
# 	def run(self,id,action):
# 		global saved_code_blocks

# 		code = saved_code_blocks[id]
# 		if action == "copy":
# 			sublime.set_clipboard(code)
# 			sublime.message_dialog("Copied code successfully")
# 		elif action == "insert":
# 			pass



class PiecesAssetIdInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		global max_assets,assets_identifiers_snapshot
		assets_list = []
		for asset_id in assets_identifiers_snapshot[:max_assets]:
			asset = get_asset_snapshot(asset_id)
			name = asset.get("name","New snippet")
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