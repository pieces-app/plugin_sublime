import sublime_plugin
import sublime
from .ask_command import copilot
from ..assets.list_assets import PiecesAssetIdInputHandler
from ..assets.assets_snapshot import AssetSnapshot


RELEVANCE_FILE_TYPES = [
	("",)
] # TODO: add the types of the files

class PiecesContextManagerCommand(sublime_plugin.TextCommand):
	def run(self, edit: sublime.Edit,context=None,pieces_asset_id=None,context_remove=None):
		if context_remove:
			key,idx = context_remove.split("_")
			idx = int(idx)
			if key == "paths":
				copilot.relevant[key].pop(idx)
			else:
				copilot.relevant[key].iterable.pop(idx)
		if pieces_asset_id:
			copilot.add_context(asset = AssetSnapshot.get_asset(pieces_asset_id))

	def is_enabled(self):
		return self.view.settings().get("PIECES_GPT_VIEW",False)
	def input(self,args):
		return PiecesContextInputHandler()


class PiecesContextInputHandler(sublime_plugin.ListInputHandler):
	def name(self):
		return "context"
	def list_items(self):
		return [
			("Add Folder","folder"),
			("Add File","file"),
			("Add a Snippet","asset"),
			*([("Show context", "show")] if copilot.relevant else []), # Show context if there is
			*([("Reset Context","reset")] if copilot.relevant else [])
		]
	def next_input(self,args):
		context = args["context"]
		if context == "file":
			sublime.open_dialog(
				lambda x:copilot.add_context(paths=list(x)) if x else None,
				multi_select=True,
			)
		elif context == "folder":
			sublime.select_folder_dialog(
				lambda x: copilot.add_context(paths=list(x)) if x else None,
				multi_select=True
			)
		elif context == "asset":
			return PiecesAssetIdInputHandler() # Choose your asset
		elif context == "reset":
			copilot.relevant = {}
		elif context == "show":
			return PiecesShowInputHandler()

class PiecesShowInputHandler(sublime_plugin.ListInputHandler):
	def name(self):
		return "context_remove"
	def list_items(self):
		res = []
		for key,value in copilot.relevant.items():
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