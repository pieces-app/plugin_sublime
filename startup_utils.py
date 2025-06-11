from ._pieces_lib.pieces_os_client.wrapper.version_compatibility import UpdateEnum, VersionChecker
from ._pieces_lib.pieces_os_client.wrapper.websockets.health_ws import HealthWS
from .settings import PiecesSettings
import sublime
from functools import wraps

PIECES_OS_MIN_VERSION = "12.0.0"  # Minimum version (12.0.0)
PIECES_OS_MAX_VERSION = "13.0.0" # Maximum version (13.0.0)

compatiablity_result = None

def check_compatiblity():
	global compatiablity_result
	if not compatiablity_result:
		pieces_os_version = PiecesSettings.api_client.version
		compatiablity_result = VersionChecker(PIECES_OS_MIN_VERSION,PIECES_OS_MAX_VERSION,pieces_os_version).version_check()
	
	return compatiablity_result


def check_pieces_os(is_input_handler=False, bypass_login=False):
	"""
		Should be annotated before each input handler and run function in each command that needs PiecesOS
	"""
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			try:
				compatiablity_result = check_compatiblity()
			except:
				compatiablity_result = None
			login_state = is_input_handler  or bypass_login or check_login()

			if compatiablity_result and not compatiablity_result.compatible:
				if not is_input_handler:
					plugin = compatiablity_result.update
					plugin_name = "PiecesOS" if plugin == UpdateEnum.PiecesOS else "Pieces for Sublime"
					r = sublime.ok_cancel_dialog(
						title="Pieces for Sublime",
						msg = (
							f"'{plugin_name}' is out of date. "
							"Please update to the latest version to ensure full functionality."
						),
						ok_title="Contact Support"
					)
					if r:
						sublime.run_command("pieces_support",args={"support":"https://docs.pieces.app/products/support"})
				return

			if PiecesSettings.api_client.is_pos_stream_running and login_state:
				return func(*args, **kwargs)
			elif PiecesSettings.api_client.is_pos_stream_running:
				return

			if PiecesSettings.api_client.is_pieces_running():
				def run_async():
					HealthWS.instance.close()
					PiecesSettings.on_settings_change()
				sublime.set_timeout_async(lambda: run_async)
				if login_state:
					return func(*args, **kwargs)
			else:
				if is_input_handler:
					return
				r = sublime.yes_no_cancel_dialog(
					title="Pieces for Sublime",
					msg=(
						"PiecesOS is not currently running.\n"
						"To use this feature, please start PiecesOS.\n"
						"Would you like to launch it now?"
					),
					yes_title="Yes",
					no_title="Contact Support",
				)
				if r == sublime.DIALOG_NO:
					return sublime.run_command("pieces_support",args={"support":"https://docs.pieces.app/products/support"})
				elif r == sublime.DIALOG_YES:
					return sublime.set_timeout_async(lambda:open_pieces_async(bypass_login ,func=func ,*args ,**kwargs))
				print("Make sure PiecesOS is running")

		return wrapper
	return decorator

def check_login() -> bool:
	from .auth.auth_user import AuthUser
	if AuthUser.user_profile:
		return True

	if sublime.ok_cancel_dialog("In order to use this feature you must be logged in. Do you want to open the login page?"):
		sublime.active_window().run_command("pieces_login")

	return False


def open_pieces_async(bypass_login:bool, *args, **kwargs):
	from .misc.open_pieces_command import PiecesOpenPiecesCommand
	running = PiecesOpenPiecesCommand.run_async()
	login_state = check_login() or bypass_login
	if running and login_state:
		func = kwargs.pop("func")
		func(*args, **kwargs)

