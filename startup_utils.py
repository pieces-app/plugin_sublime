from ._pieces_lib.pieces_os_client.wrapper.version_compatibility import UpdateEnum, VersionChecker
from ._pieces_lib.pieces_os_client.wrapper.websockets.health_ws import HealthWS
from .settings import PiecesSettings
import sublime
from functools import wraps
import threading

PIECES_OS_MIN_VERSION = "10.1.5"  # Minimum version (10.1.5)
PIECES_OS_MAX_VERSION = "11.0.0" # Maximum version (11.0.0)

compatiablity_result = None

def check_compatiblity():
	global compatiablity_result
	if not compatiablity_result:
		pieces_os_version = PiecesSettings.api_client.version
		compatiablity_result = VersionChecker(PIECES_OS_MIN_VERSION,PIECES_OS_MAX_VERSION,pieces_os_version).version_check()
	
	return compatiablity_result


def check_pieces_os(is_input_handler=False):
	"""
		Should be annotated before each input handler and run function in each command that needs Pieces OS
	"""
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			try:
				compatiablity_result = check_compatiblity()
			except:
				compatiablity_result = None

			if compatiablity_result and not compatiablity_result.compatible:
				if not is_input_handler:
					plugin = compatiablity_result.update
					plugin_name = "Pieces OS" if plugin == UpdateEnum.PiecesOS else "Pieces for Sublime"
					sublime.error_message(f"'{plugin_name}' is out of date. Please update to the latest version to ensure full functionality.")
				return

			if HealthWS.instance.is_loaded:
				return func(*args, **kwargs)

			if PiecesSettings.api_client.is_pieces_running():
				def run_async():
					HealthWS.instance.close()
					PiecesSettings.on_settings_change(True)
				sublime.set_timeout_async(lambda: run_async)
				return func(*args, **kwargs)
			else:
				if is_input_handler:
					return
				r = sublime.yes_no_cancel_dialog(
					title="Pieces for Sublime",
					msg=(
				        "Pieces OS is not currently running.\n"
				        "To use this feature, please start Pieces OS.\n"
				        "Would you like to launch it now?"
				    ),
					yes_title="Yes",
					no_title="Contact Support",
				)
				if r == sublime.DIALOG_NO:
					return sublime.run_command("pieces_support",args={"support":"https://docs.pieces.app/support"})
				elif r == sublime.DIALOG_YES:
					return sublime.run_command("pieces_open_pieces")
				print("Make sure Pieces OS is running")

		return wrapper
	return decorator

