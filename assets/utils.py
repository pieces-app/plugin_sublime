import queue
from typing import Dict
import threading
from pieces_os_client import Asset, AssetApi,StreamedIdentifiers
import sublime

from pieces.settings import PiecesSettings


class AssetSnapshot:
	assets_identifiers_snapshot = [] # List of all the assets id that the user have
	assets_snapshot:Dict[str,Asset] = {}  # List of the asset object that is already loaded
	loaded_assets_identifiers_snapshot = [] # List of the loaded ids that is in the assets_snpashot 
	asset_queue = queue.Queue() # Queue for asset_ids to be processed
	block = True # to wait for the queue to recevive the first asset id
	asset_set = set()  # Set for asset_ids in the queue


	@classmethod
	def worker(cls):
		try:
			while True:
				asset_id = cls.asset_queue.get(block=cls.block,timeout=5)
				cls.update_asset_id(asset_id)
				cls.asset_queue.task_done()
				cls.asset_set.remove(asset_id)  # Remove asset_id from the set
		except queue.Empty: # queue is empty and the block is false
			if cls.block:
				cls.worker() # if there is more assets to load
			return # End the worker



	@classmethod
	def update_asset_id(cls,asset_id):
		api_instance = AssetApi(PiecesSettings.api_client)
		asset = api_instance.asset_snapshot(asset_id)
		cls.assets_snapshot[asset_id] = asset
		if asset_id not in cls.loaded_assets_identifiers_snapshot:
			cls.loaded_assets_identifiers_snapshot.append(asset_id) # Display only the loaded assets

	@classmethod
	def assets_snapshot_callback(cls,ids:StreamedIdentifiers):
		# Start the worker thread if it's not running
		cls.block = True
		sublime.set_timeout_async(cls.worker)
		for item in ids.iterable:
			asset_id = item.asset.id
			if asset_id not in cls.assets_identifiers_snapshot:
				cls.assets_identifiers_snapshot.append(asset_id)
			if asset_id not in cls.asset_set:
				if item.deleted:
					# Asset deleted
					cls.assets_identifiers_snapshot.remove(asset_id)
					cls.loaded_assets_identifiers_snapshot.remove(asset_id)
					cls.assets_snapshot.pop(asset_id)
				else:
					cls.asset_queue.put(asset_id)  # Add asset_id to the queue
					cls.asset_set.add(asset_id)  # Add asset_id to the set
		cls.block = False # Remove the block to end the thread







def tabulate_from_markdown(md_text):
	# Split the markdown text into lines
	lines = md_text.split('\n')

	# Filter out lines that contain '|', and join them back into a string
	table_md = "\n".join(line for line in lines if '|' in line)

	# Split the markdown table into lines, and then into cells
	# Also, remove leading/trailing whitespace from each cell
	data = [[cell.strip() for cell in line.split("|")[1:-1]] for line in table_md.strip().split("\n")]

	headers = "<div>"
	for header in data[0]:
		if header:
			headers += "<span><h1>" + header + "</h1></span>"

    # Generate HTML string
	html_text = f"{headers}</div><br><div>"
	for row in data[2:]:
		html_text += "<div>"
		for idx,cell in enumerate(row):
			if idx == 0:
				cell += ": " 
			html_text += "<span>" + cell + "</span>"
		html_text += "<br><br></div>"
	html_text += "</div>"


	return md_text.replace(table_md,html_text)