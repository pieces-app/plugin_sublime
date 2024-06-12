import queue
from typing import Dict,TypeVar
from pieces_os_client import StreamedIdentifiers
import sublime

# Define a type variable that matches the return type of api_call
T = TypeVar('T')


class StreamedIdentifiersCache:
	"""
		This class is made for caching Streamed Identifiers.
		Please use this class only as a parent class
	"""	

	def __init_subclass__(cls, api_call,**kwargs):
		super().__init_subclass__(**kwargs)
		cls.identifiers_snapshot: Dict[str, T] = {}  # Map id:return from the api_call
		cls.identifiers_queue = queue.Queue()  # Queue for ids to be processed
		cls.identifiers_set = set()  # Set for ids in the queue
		cls.api_call = api_call
		cls.block = True  # to wait for the queue to receive the first id
		cls.first_shot = True  # First time to open the websocket or not


	@classmethod
	def worker(cls):
		try:
			while True:
				id = cls.identifiers_queue.get(block=cls.block,timeout=5)
				cls.identifiers_set.remove(id)  # Remove the id from the set
				cls.update_identifier(id)
				cls.identifiers_queue.task_done()
		except queue.Empty: # queue is empty and the block is false
			if cls.block:
				cls.worker() # if there is more ids to load
			return # End the worker

	
	@classmethod
	def update_identifier(cls,id) -> T:
		id_value = api_call(id)
		cls.identifiers_snapshot[id] = id_value
		return id_value

	@classmethod
	def streamed_identifiers_callback(cls,ids:StreamedIdentifiers):
		# Start the worker thread if it's not running
		cls.block = True
		sublime.set_timeout_async(cls.worker)
		for item in ids.iterable:
			reference_item = getattr(item,"asset",item.conversation) # Get either the conversation or the asset
			if id not in cls.identifiers_set:
				if item.deleted:
					# Asset deleted
					try:
						cls.identifiers_snapshot.pop(id)
					except KeyError:
						pass
				else:
					if id not in cls.identifiers_snapshot and not cls.first_shot:
						cls.identifiers_snapshot = {id:None,**cls.identifiers_snapshot}
					cls.identifiers_queue.put(id)  # Add id to the queue
					cls.identifiers_set.add(id)  # Add id to the set
		cls.first_shot = False
		cls.block = False # Remove the block to end the thread

