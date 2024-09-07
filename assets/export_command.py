import sublime_plugin
import mdpopups
import os
import re
from .._pieces_lib.typing_extensions import Self
from .._pieces_lib.pieces_os_client.wrapper.basic_identifier.asset import BasicAsset
from .list_assets import PiecesAssetIdInputHandler,A_TAG_STYLE
from .ext_map import file_map
from ..settings import PiecesSettings

template_snippet = """<snippet>
<!-- asset_id {asset_id} -->
<!--
	This Snippet is generated via Pieces Sublime Plugin!
	For more info: 
	- https://www.sublimetext.com/docs/completions.html#snippets
	- https://www.sublimetext.com/docs/selectors.html
-->

<!-- WARNING don't remove the above tags -->

<content><![CDATA[
{content}
]]></content>
<tabTrigger>{trigger}</tabTrigger>
<description>{description}</description>
<scope>{scope}</scope>
</snippet>"""

template_view = """
# Creating a Sublime Snippet
```{lang}
{content}
```

- Tab Trigger: <a href='subl:pieces_edit_snippet_sheet {{"field":"trigger","sheet_id":{sheet_id}}}'>{trigger}</a>

- Description: <a href='subl:pieces_edit_snippet_sheet {{"field":"description","sheet_id":{sheet_id}}}'>{description}</a>

- Scope: <a href='subl:pieces_edit_snippet_sheet {{"field":"scope","sheet_id":{sheet_id}}}'>{scope}</a>

For more info about scopes and snippets visit:

- https://www.sublimetext.com/docs/completions.html#snippets
- https://www.sublimetext.com/docs/selectors.html

<a style="{A_TAG_STYLE}" href='subl:pieces_save_sublime_snippet {{"sheet_id":{sheet_id}}}'>Save</a>
"""
class PiecesExportAssetToSublimeCommand(sublime_plugin.WindowCommand):
	_instances = []
	def __init__(self, window):
		PiecesExportAssetToSublimeCommand._instances.append(self)
		super().__init__(window)

	def input(self, args: dict):
		return PiecesAssetIdInputHandler()

	def run(self,pieces_asset_id):
		asset_wrapper = BasicAsset(pieces_asset_id)
		self.trigger = asset_wrapper.name
		self.asset_description = asset_wrapper.description if asset_wrapper.description else "No description found"

		self.content = asset_wrapper.raw_content
		
		self.dummy_view = self.window.create_output_panel("pieces_dummy_view",unlisted=True)
		self.lang = asset_wrapper.classification
		self.asset_id = pieces_asset_id

		try: syntax = file_map[self.lang]
		except: syntax=None

		if syntax:
			self.dummy_view.assign_syntax(syntax = syntax)

		self.dummy_view.run_command("append",{"characters":self.content})
		self.scope = self.dummy_view.scope_name(
			10 # ignoring the content at the begining
		).strip().replace(' ', ', ')

		self.sheet = mdpopups.new_html_sheet(self.window,asset_wrapper.name,contents="")
		self.update_sheet()

	def update_sheet(self):
		mdpopups.update_html_sheet(
			self.sheet,
			template_view.format(
				trigger = self.trigger,
				asset_id = self.asset_id,
				content = self.content,
				description = self.asset_description,
				scope = self.scope,
				lang = self.lang.value if self.lang else "txt",
				A_TAG_STYLE = A_TAG_STYLE,
				sheet_id =self.sheet.id()
			),
			wrapper_class="wrapper",
			css=".wrapper {margin-left:6px}")	

	def __str__(self):
		return str(self.sheet.id())

	@classmethod
	def get_instance(cls,sheet_id) -> Self:
		return [instance for instance in cls._instances if str(instance) == str(sheet_id)][-1] # Return the last instance

	def close_sheet(self):
		self.sheet.close(lambda x:self._instances.remove(self))

	def is_enabled(self):
		return PiecesSettings.is_loaded

class PiecesSaveSublimeSnippetCommand(sublime_plugin.WindowCommand):
	SNIPPETS_DIR = os.path.join(PiecesSettings.PIECES_USER_DIRECTORY, "snippets")
	def run(self,sheet_id):
		instance = PiecesExportAssetToSublimeCommand.get_instance(sheet_id)
		kwargs={
			"asset_id":instance.asset_id,
			"content":instance.content,
			"description":instance.description,
			"scope":instance.scope,
			"trigger":instance.trigger
		}
		if not os.path.exists(self.SNIPPETS_DIR):
			os.makedirs(self.SNIPPETS_DIR)
		name = kwargs["trigger"]
		name = re.sub(r'[\\/*?:"<>|]', '', name)
		dir_name = os.path.join(self.SNIPPETS_DIR,f'{name}.sublime-snippet')
		with open(dir_name,"w") as f:
			f.write(template_snippet.format(**kwargs))
		instance.close_sheet()

	def is_enabled(self):
		return PiecesSettings.is_loaded

class PiecesEditSnippetSheetCommand(sublime_plugin.WindowCommand):
	def run(self,field:str,sheet_id):
		"""
			field (str):
				- trigger
				- scope
				- description
				- content
				- asset_id
		"""
		self.field = field
		self.instance = PiecesExportAssetToSublimeCommand.get_instance(sheet_id)
		self.window.show_input_panel(f"{field.title()}:", getattr(self.instance,field), self.on_done, None, None)

	def on_done(self, user_response):
		setattr(self.instance,self.field,user_response)
		self.instance.update_sheet()

	def is_enabled(self):
		return PiecesSettings.is_loaded

