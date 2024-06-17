import sublime_plugin
import sublime
from pieces_os_client import *

from .list_assets import PiecesListAssetsCommand
from .ext_map import file_map


class PiecesHandleMarkdownCommand(sublime_plugin.WindowCommand):
	
	def run(self,mode,sheet_id=None):
		
		self.sheet_id = sheet_id
		
		if not sheet_id:
			self.sheet_id = self.window.active_view().settings().get("pieces_sheet_id")

		self.sheet = sublime.Sheet(self.sheet_id)
		

		sheet_details = None
		if self.sheet_id:
			self.sheet_details = PiecesListAssetsCommand.sheets_md.get(sheet_id)

		if not sheet_details:
			return

		
		self.code = sheet_details["code"]
		self.language = sheet_details["language"]
		self.name = sheet_details["name"]
		self.asset_id = sheet_details["id"]

		if mode == "copy":
			sublime.set_clipboard(self.code)
		elif mode == "edit":
			self.handle_edit()
		elif mode == "delete":
			self.window.run_command("pieces_delete_asset")
		if mode == "save":
			data = self.window.active_view().substr(sublime.Region(0, self.window.active_view().size()))
			self.window.run_command("pieces_save_asset",args={"asset_id":self.asset_id,"data":data})


	def handle_edit(self):
		# Create a new file
		view = self.window.new_file()
		
		if self.language:
			syntax = file_map.get(self.language)
			if syntax:
				view.assign_syntax(syntax = syntax)
		# Insert the text
		view.run_command('append', {'characters': self.code})
		# Set the name
		view.set_name(self.name)
		# Set it to scratch to avoid the default saving menu
		view.set_scratch(True)
		# Set the view to handle the save operation
		view.settings().set("pieces_sheet_id",self.sheet_id)
		# Close the sheet
		self.sheet.close()



