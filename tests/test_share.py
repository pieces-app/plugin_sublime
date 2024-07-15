from UnitTesting.unittesting import DeferrableTestCase
import sublime

from Pieces.assets.share_asset import PiecesShareAssetCommand
from Pieces.assets.assets_snapshot import AssetSnapshot

class TestShareCommand(DeferrableTestCase):
	def setUp(self):
		self.window = sublime.active_window()
		self.main_views = self.window.views(include_transient=True)
		self.view = self.window.new_file()
		self.command = PiecesShareAssetCommand(self.window)
		yield 3000 # Wait 3 sec for everything to load (websockets)
		self.asset_id = list(AssetSnapshot.identifiers_snapshot.keys())[0]
		self.inital_shares_len = self.get_shares_len()
		print(self.inital_shares_len)

	def tearDown(self):
		if self.view:
			self.view.close()

	def get_shares_len(self):
		return len(AssetSnapshot.identifiers_snapshot[self.asset_id].shares.iterable)
		
	def disconnect_cloud(self):
		self.window.run_command("pieces_allocation_disconnect")

	def connect_cloud(self):
		self.window.run_command("pieces_allocation_connect")

	def test_share(self):
		self.command.run(self.asset_id)
		

	def test_share_disconnect_cloud(self):
		"""
			Test the shares API when the cloud is disconnected
		"""
		self.disconnect_cloud()
		self.test_share()
		yield 10000 # Wait for the shareable link to be generated
		self.assertEqual(self.get_shares_len(),self.inital_shares_len)

	def test_share_connect_cloud(self):
		"""
			Test the shares API when the cloud is Connected
		"""
		self.connect_cloud()
		yield 5000
		self.test_share()
		yield 10000 # Wait for the shareable link to be generated
		self.assertEqual(self.get_shares_len(),self.inital_shares_len+1)

