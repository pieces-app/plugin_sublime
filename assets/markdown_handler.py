import sublime_plugin
import sublime
from .list_assets import PiecesListAssetsCommand
from .utils import AssetSnapshot
from pieces_os_client import *

from pieces.settings import PiecesSettings

class PiecesHandleMarkdownCommand(sublime_plugin.WindowCommand):
	views_to_handle = {}
	def run(self,mode):
		sheet = self.window.active_sheet()
		self.sheet = sheet
		sheet_details = None
		if sheet:
			sheet_details = PiecesListAssetsCommand.sheets_md.get(sheet.id())
		
		if mode == "save":
			self.handle_save()
		
		if not sheet_details:
			if mode == "copy":
				self.window.run_command("copy") # Default copy command
			if mode == "delete":
				self.window.run_command("right_delete") # Default delete key
			return

		self.code = sheet_details["code"]
		self.language = sheet_details["language"]
		self.name = sheet_details["name"]
		self.asset_id = sheet_details["id"]

		if mode == "copy":
			self.handle_copy()
		elif mode == "edit":
			self.handle_edit()
		elif mode == "delete":
			self.window.run_command("pieces_delete_asset")



	def handle_save(self):
		view = self.window.active_view()
		if view:
			asset_id = PiecesHandleMarkdownCommand.views_to_handle.get(view.id())
			if asset_id:
				asset = AssetSnapshot.assets_snapshot[asset_id]
				format_api = FormatApi(PiecesSettings.api_client)
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
				self.sheet.close(lambda x: view.close(on_close=lambda x:self.window.run_command("pieces_list_assets",{"pieces_asset_id":asset_id})))
			else:
				self.window.run_command("save")

	def handle_copy(self):
		sublime.set_clipboard(self.code)
	def handle_edit(self):
		# Create a new file
		view = self.window.new_file()
		if self.language:
			syntax_file = f'{self.language}.sublime-syntax'
			available_syntaxes = sublime.find_resources("*.sublime-syntax")
			for syntax in available_syntaxes:
				if syntax_file in syntax:
					view.assign_syntax(syntax = syntax)
					break
		# Insert the text
		view.run_command('insert', {'characters': self.code})
		# Set the name
		view.set_name(self.name)
		# Set it to avoid the saving dialog 
		view.set_scratch(True)
		# Set the view to handle the save operation
		PiecesHandleMarkdownCommand.views_to_handle[view.id()] = self.asset_id
		# Close the sheet
		self.sheet.close()



