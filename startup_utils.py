from ._pieces_lib.pieces_os_client.wrapper.version_compatibility import UpdateEnum
from .settings import PiecesSettings
import sublime



def check_pieces_os(func):
	def wrapper(*args, **kwargs):
		if PiecesSettings.is_loaded:
			return func(*args, **kwargs)

		if not PiecesSettings.compatiablity_result.compatible:
			plugin = PiecesSettings.compatiablity_result.update
			plugin_name = "Pieces OS" if plugin == UpdateEnum.PiecesOS else "Pieces for Sublime"
			print(f"Please update {plugin_name}")

		if PiecesSettings.compatiablity_result.compatible:
			def run_async():
				if PiecesSettings.api_client.is_pieces_running():
					PiecesSettings.on_settings_change(True)
					return func(*args,**kwargs)
			sublime.set_timeout_async(run_async)
			print("Make sure Pieces OS is running")
		
	return wrapper


def check_input_handler(func):
	def wrapper(*args, **kwargs):
		if PiecesSettings.is_loaded:
			return func(*args, **kwargs)

		if not PiecesSettings.compatiablity_result.compatible:
			return 

		if PiecesSettings.compatiablity_result.compatible:
			def run_async():
				if PiecesSettings.api_client.is_pieces_running():
					PiecesSettings.on_settings_change(True)
					return func(*args,**kwargs)
			sublime.set_timeout_async(run_async)
		
	return wrapper

