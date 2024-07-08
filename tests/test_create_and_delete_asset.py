from UnitTesting.unittesting import DeferrableTestCase
from unittest.mock import patch
import sublime

from Pieces.assets.create_asset import PiecesCreateAssetCommand
from Pieces.assets.assets_snapshot import AssetSnapshot

class TestCreateAndDeleteCommand(DeferrableTestCase):
	def setUp(self):
		self.window = sublime.active_window()
		self.main_views = self.window.views(include_transient=True)
		self.view = self.window.new_file()
		self.command = PiecesCreateAssetCommand(self.view)
		yield 3000 # Wait 3 sec for everythin to load (websockets)
		self.text_asset = """import requests\nrequests.get("https://pieces.app")"""

	def tearDown(self):
		if self.view:
			self.view.close()
		[view.close() for view in self.window.views() if view not in self.main_views] # Clean the views


	def test_create_command(self):
		self.view.run_command("pieces_create_asset",args={"data":self.text_asset})
		yield 1000

		TestCreateAndDeleteCommand.asset_id = list(AssetSnapshot.identifiers_snapshot.keys())[0]
		raw = AssetSnapshot.identifiers_snapshot[TestCreateAndDeleteCommand.asset_id].original.reference.fragment.string.raw

		self.assertEqual(raw,self.text_asset)

	@patch('sublime.ok_cancel_dialog', return_value=True)
	def test_delete_command(self,mock_ok_cancel):
		self.window.run_command("pieces_delete_asset")
		yield 500
		self.assertIsNone(AssetSnapshot.identifiers_snapshot.get(TestCreateAndDeleteCommand.asset_id))
