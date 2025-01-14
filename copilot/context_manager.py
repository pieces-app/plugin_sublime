import sublime_plugin
import sublime
from .ask_command import copilot
from .._pieces_lib.pieces_os_client.wrapper.basic_identifier.asset import BasicAsset
from ..settings import PiecesSettings
from ..startup_utils import check_pieces_os
from ..assets.list_assets import PiecesAssetIdInputHandler

class PiecesContextManagerCommand(sublime_plugin.WindowCommand):
	@check_pieces_os()
	def run(self,context,pieces_asset_id=None,context_remove=None):
		if context_remove:
			key,idx = context_remove.split("_")
			idx = int(idx)
			if key == "paths":
				PiecesSettings.api_client.copilot.context.paths.pop(idx)
			elif key == "seeds":
				PiecesSettings.api_client.copilot.context.raw_assets.pop(idx)
			elif key == "assets":
				PiecesSettings.api_client.copilot.context.assets.pop(idx)

		if pieces_asset_id:
			PiecesSettings.api_client.copilot.context.assets.append(BasicAsset(pieces_asset_id))

	def is_enabled(self):
		v = sublime.active_window().active_view()
		if v:
			return v.settings().get("PIECES_GPT_VIEW",False)
		return False

	@check_pieces_os(True)
	def input(self,args):
		return PiecesContextInputHandler()


class PiecesContextInputHandler(sublime_plugin.ListInputHandler):
	def name(self):
		return "context"
	def list_items(self):
		relevance_exists = PiecesSettings.api_client.copilot.context._check_relevant_existence()

		return [
			("Add Folder","folder"),
			("Add File","file"),
			("Add a Snippet","asset"),
			*([("Show context", "show")] if relevance_exists else []), # Show context if there is
			*([("Reset Context","reset")] if relevance_exists else [])
		]
	def next_input(self,args):
		context = args["context"]
		if context == "file":
			sublime.open_dialog(
				self.append_path,
				multi_select=True,
			)
		elif context == "folder":
			sublime.select_folder_dialog(
				self.append_path,
				multi_select=True
			)
		elif context == "asset":
			return PiecesAssetIdInputHandler() # Choose your asset
		elif context == "reset":
			PiecesSettings.api_client.copilot.context.clear()
		elif context == "show":
			return PiecesShowInputHandler()
	
	@staticmethod
	def append_path(paths):
		if isinstance(paths,list):
			PiecesSettings.api_client.copilot.context.paths.extend(paths)
		elif isinstance(paths,str):
			PiecesSettings.api_client.copilot.context.paths.append(paths)

class PiecesAddContextCommand(sublime_plugin.ApplicationCommand):
	@check_pieces_os()
	def run(self,paths = None):
		if paths == None:
			paths = [sublime.active_window().active_view().file_name()]
			if paths[0] == None: return # check the file already exists

		if not copilot._gpt_view: # check if the Copilot is running
			copilot.render_conversation(None) # Create a new conversation
		PiecesSettings.api_client.copilot.context.paths.extend(paths)


class PiecesShowInputHandler(sublime_plugin.ListInputHandler):
	def name(self):
		return "context_remove"

	def list_items(self):
		res = []
		context = PiecesSettings.api_client.copilot.context

		for key,value in {"paths":context.paths, "seeds":context.raw_assets, "assets":context.assets}.items():
			if key == "paths":
				for idx,path in enumerate(value):
					res.append((path,f"paths_{idx}"))
			elif key == "assets":
				for idx,asset in enumerate(value):
					res.append((asset.name,f"assets_{idx}"))
			elif key == "seeds":
				for idx in range(len(value)):
					res.append((f"Snippet {idx+1}",f"seeds_{idx}"))
		return res


	def placeholder(self) -> str:
		return "Select the context to remove it"