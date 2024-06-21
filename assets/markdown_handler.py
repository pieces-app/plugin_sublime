import sublime_plugin
import sublime
from .._pieces_lib.pieces_os_client import *

from .list_assets import PiecesListAssetsCommand
from .ext_map import file_map


class PiecesHandleMarkdownCommand(sublime_plugin.WindowCommand):
	
	def run(self,mode,sheet_id=None,data=None,close=True):
		"""
		Executes various operations on a sheet based on the specified mode.

		Parameters:
		mode (str): The operation mode. Can be one of the following:
		    - "copy": Copies the sheet's code to the clipboard.
		    - "edit": Initiates the edit process for the sheet.
		    - "delete": Deletes the sheet.
		    - "save": Saves the provided data to the sheet.
		    - "share": Shares the sheet by generating a shareable link.
		sheet_id (int, optional): The ID of the sheet to operate on. If not provided, it will be fetched from the active view's settings.
		data (str, optional): The data to save to the sheet. Only used when mode is "save".
		close (str,optional): Close the view after saving in the save mode?

		Returns:
		None
		"""
		
		self.sheet_id = sheet_id
		if not self.sheet_id:
			self.sheet_id = self.window.active_view().settings().get("pieces_sheet_id")
			del self.window.active_view().settings()["pieces_sheet_id"]
		
		self.sheet_id = int(self.sheet_id)
		self.sheet = sublime.Sheet(self.sheet_id)

		sheet_details = None
		if self.sheet_id:
			sheet_details = PiecesListAssetsCommand.sheets_md.get(self.sheet_id)

		if not sheet_details:
			return
		
		self.code = sheet_details["code"]
		self.language = sheet_details["language"]
		self.name = sheet_details["name"]
		self.asset_id = sheet_details["id"]

		if mode == "copy":
			sublime.set_clipboard(self.code)
			PiecesListAssetsCommand.update_sheet(self.sheet,self.asset_id,{"copy":"Copied"})
		elif mode == "edit":
			self.handle_edit()
		elif mode == "delete":
			self.window.run_command("pieces_delete_asset")
		elif mode == "save":
			view = self.window.active_view()
			if not data:
				data = view.substr(sublime.Region(0, self.window.active_view().size()))
			self.window.run_command("pieces_save_asset",args={"asset_id":self.asset_id,"data":data})
			
			if close:
				view.close(lambda x: self.window.run_command("pieces_list_assets",{"pieces_asset_id":self.asset_id}))
			
		elif mode == "share":
			PiecesListAssetsCommand.shareable_link.append(self.asset_id)
			self.window.run_command("pieces_share_asset",args={"asset_id":self.asset_id,"update_sheet":True})
	


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



