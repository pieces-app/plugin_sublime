from UnitTesting.unittesting import DeferrableTestCase
import sublime

from Pieces.assets.create_asset import PiecesCreateAssetCommand
from Pieces.assets.utils import AssetSnapshot

class TestListAssetsCommand(DeferrableTestCase):
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

		TestListAssetsCommand.asset_id = list(AssetSnapshot.assets_snapshot.keys())[0]
		raw = AssetSnapshot.assets_snapshot[TestListAssetsCommand.asset_id].original.reference.fragment.string.raw

		self.assertEqual(raw,self.text_asset)


	def test_delete_command(self):
		self.view.run_command("pieces_delete_asset",args={"asset_id":TestListAssetsCommand.asset_id})
		yield 3000

		self.assertIsNone(AssetSnapshot.assets_snapshot.get(TestListAssetsCommand.asset_id))
