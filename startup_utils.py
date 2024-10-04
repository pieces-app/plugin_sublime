from ._pieces_lib.pieces_os_client.wrapper.version_compatibility import UpdateEnum
from .settings import PiecesSettings
import sublime
from functools import wraps

def check_pieces_os(is_input_handler=False):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			if PiecesSettings.is_loaded:
				return func(*args, **kwargs)

			if not PiecesSettings.compatiablity_result.compatible:
				if not is_input_handler:
					plugin = PiecesSettings.compatiablity_result.update
					plugin_name = "Pieces OS" if plugin == UpdateEnum.PiecesOS else "Pieces for Sublime"
					print(f"Please update {plugin_name}")
				return

			if PiecesSettings.api_client.is_pieces_running():
				sublime.set_timeout_async(lambda: PiecesSettings.on_settings_change(True))
				return func(*args, **kwargs)
			else:
				print("Make sure Pieces OS is running")

		return wrapper
	return decorator

