import sublime_plugin
import sublime
from .._pieces_lib.pieces_os_client.wrapper.basic_identifier.asset import BasicAsset
from ..settings import PiecesSettings
from ..assets.list_assets import PiecesAssetIdInputHandler


class PiecesContextManagerCommand(sublime_plugin.TextCommand):
	def run(self, edit: sublime.Edit,context=None,pieces_asset_id=None,context_remove=None):
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
		return self.view.settings().get("PIECES_GPT_VIEW",False) and PiecesSettings.is_loaded
	def input(self,args):
		return PiecesContextInputHandler()


class PiecesContextInputHandler(sublime_plugin.ListInputHandler):
	def name(self):
		return "context"
	def list_items(self):
		relevance_exists = PiecesSettings.api_client.copilot.context._check_relevant_existance()
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
			for path in paths:
				PiecesSettings.api_client.copilot.context.paths.append(path)
		elif isinstance(paths,str):
			PiecesSettings.api_client.copilot.context.paths.append(paths)

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
				for idx,asset in enumerate(value.iterable):
					res.append((asset.name,f"assets_{idx}"))
			elif key == "seeds":
				for idx in range(len(value.iterable)):
					res.append((f"Snippet {idx+1}",f"seeds_{idx}"))
		return res


	def placeholder(self) -> str:
		return "Select the context to remove it"