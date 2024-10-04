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
					sublime.error_message(f"'{plugin_name}' is out of date. Please update to the latest version to ensure full functionality.")
				return

			if PiecesSettings.api_client.is_pieces_running():
				sublime.set_timeout_async(lambda: PiecesSettings.on_settings_change(True))
				return func(*args, **kwargs)
			else:
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
					sublime.run_command("pieces_support")
				elif r == sublime.DIALOG_YES:
					return sublime.run_command("pieces_open_pieces")
				print("Make sure Pieces OS is running")

		return wrapper
	return decorator

