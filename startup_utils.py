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
			# Step 1: Check compatibility first
			try:
				compatiablity_result = check_compatiblity()
			except:
				compatiablity_result = None

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

			# Step 2: Check if PiecesOS is running
			if not PiecesSettings.api_client.is_pieces_running():
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
					return sublime.set_timeout_async(lambda: open_pieces_async(bypass_login, func, *args, **kwargs))
				return

			# Step 3: Handle PiecesOS stream status
			if not PiecesSettings.api_client.is_pos_stream_running:
				# PiecesOS is running but stream needs restart
				def restart_stream():
					HealthWS.instance.close()
					PiecesSettings.on_settings_change()
				sublime.set_timeout_async(restart_stream)

			# Step 4: Check login state (only if not bypassed)
			if not bypass_login and not is_input_handler:
				login_state = check_login()
				if not login_state:
					return

			# Step 5: Execute the function if all checks pass
			if PiecesSettings.api_client.is_pos_stream_running or PiecesSettings.api_client.is_pieces_running():
				return func(*args, **kwargs)

		return wrapper
	return decorator

def check_login() -> bool:
	from .auth.auth_user import AuthUser
	if AuthUser.user_profile:
		return True

	if sublime.ok_cancel_dialog("Please sign into Pieces to use this feature. Do you want to sign in now?"):
		sublime.active_window().run_command("pieces_login")
		return False  # Return False since login is async

	return False


def open_pieces_async(bypass_login: bool, func, *args, **kwargs):
	from .misc.open_pieces_command import PiecesOpenPiecesCommand
	from .auth.auth_user import AuthUser
	
	# Try to launch PiecesOS (without showing duplicate dialog)
	running = PiecesOpenPiecesCommand.run_async(show_dialog=False)
	AuthUser.user_profile = PiecesSettings.api_client.user_api.user_snapshot().user
	
	if running:
		# Check login state if not bypassed
		if not bypass_login:
			login_state = check_login()
			if not login_state:
				return
		
		# Execute the original function
		func(*args, **kwargs)
	else:
		# Show install dialog only once, from here
		if sublime.ok_cancel_dialog("PiecesOS could not be launched. Would you like to install it?"):
			sublime.active_window().run_command("pieces_install_pieces_os")

