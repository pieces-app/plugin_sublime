from UnitTesting.unittesting import DeferrableTestCase
import sublime

from Pieces.assets.list_assets import PiecesListAssetsCommand
from Pieces.assets.markdown_handler import PiecesHandleMarkdownCommand
from Pieces.assets.utils import AssetSnapshot


class TestListAssetsCommand(DeferrableTestCase):
	def setUp(self):
		self.test_text = "\n# This is added via the test in the sublime plugin"
		self.window = sublime.active_window()
		self.main_views = self.window.views(include_transient=True)
		self.view = self.window.new_file()
		self.command = PiecesHandleMarkdownCommand(self.window)
		yield 3000 # Wait 3 sec for everythin to load (websockets)
		self.asset_id = list(AssetSnapshot.assets_snapshot.keys())[0] # id to test on


	def tearDown(self):
		if self.view:
			self.view.close()
		[view.close() for view in self.window.views() if view not in self.main_views] # Clean the viewss

	def test_edit_command(self):
		PiecesListAssetsCommand(self.window).run(self.asset_id) # Open a sheet to test on
		yield 500 # wait until the command run
		self.command.run("edit")
		yield 1000
		edited_view = self.window.active_view()
		sheet_id = list(PiecesListAssetsCommand.sheets_md.keys())[0]
		code = PiecesListAssetsCommand.sheets_md[sheet_id]["code"]
		
		yield 500
		self.assertEqual(edited_view.substr(
				sublime.Region(0,edited_view.size())
			),code) # Make sure the code is correctly entered

		edited_view.run_command("append",{"characters":self.test_text})
		self.command.run("save") # Save the changes

		yield 500 # Wait some until the changes recevied by the websocket

		code = AssetSnapshot.assets_snapshot[self.asset_id].original.reference.fragment.string.raw

		self.assertTrue(code.endswith(self.test_text)) # Make sure the code edited properly 

