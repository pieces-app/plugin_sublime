from UnitTesting.unittesting import DeferrableTestCase
import sublime
from Pieces.assets.list_assets import PiecesListAssetsCommand
from Pieces.assets.assets_snapshot import AssetSnapshot


class TestListAssetsCommand(DeferrableTestCase):
	def setUp(self):
		self.window = sublime.active_window()
		self.main_views = self.window.views(include_transient=True)
		self.view = self.window.new_file()
		self.command = PiecesListAssetsCommand(self.window)
		yield 3000 # Wait 3 sec for everythin to load (websockets)

	def tearDown(self):
		if self.view:
			self.view.close()
		[view.close() for view in self.window.views() if view not in self.main_views] # Clean the views

	def test_assets_list(self):
		assets = self.command.input(args={}).list_items()
		self.assertIsInstance(assets, list)
		self.assertGreater(len(assets), 0)


	def test_run_command(self):
		self.command.run(list(AssetSnapshot.identifiers_snapshot.keys())[0]) # Open the first asset
		yield 500 # wait for the command to run
		sheet_id = list(PiecesListAssetsCommand.sheets_md.keys())[0]
		# Make sure the correct asset is generate successfully
		self.assertEqual(len([sheet for sheet in self.window.sheets() if sheet.id() == sheet_id]),1)


