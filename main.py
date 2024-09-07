from . import __version__
from .settings import PiecesSettings
from .copilot.ask_command import copilot
import sublime
from ._pieces_lib.pieces_os_client.wrapper.version_compatibility import VersionChecker,UpdateEnum
from ._pieces_lib.pieces_os_client.wrapper.websockets import BaseWebsocket,AuthWS,HealthWS

# load the commands
from .assets import *
from .ask import *
from .auth import *
from .search import *
from .misc import *
from .copilot import *

PIECES_OS_MIN_VERSION = "10.1.5"  # Minimum version (10.1.5)
PIECES_OS_MAX_VERSION = "11.0.0" # Maximum version (11.0.0)


def startup():
	pieces_os_version = PiecesSettings.api_client.version
	version_result = VersionChecker(PIECES_OS_MIN_VERSION,PIECES_OS_MAX_VERSION,pieces_os_version).version_check()
	if version_result.compatible:
		print(f"Pieces OS version: {pieces_os_version}\nPlugin version: {__version__}")
		PiecesSettings.models_init(PiecesSettings.get_settings().get('model')) # Intilize the models
	else: 
		if version_result.update == UpdateEnum.PiecesOS:
			update = "Pieces OS"
		else:
			update = "Pieces Sublime Plugin"
		sublime.message_dialog(f"{update} is outdated. Can you please update {update}")
		PiecesSettings.is_loaded = False
		BaseWebsocket.close_all()
		return
	
	# User Weboscket
	PiecesSettings.create_auth_output_panel()

	PiecesSettings.api_client.user.on_user_callback = AuthUser.on_user_callback

	# Lunch Onboarding if it is the first time
	if not PiecesOnboardingCommand.get_onboarding_settings().get("lunch_onboarding",False):
		sublime.active_window().run_command("pieces_onboarding")
		PiecesOnboardingCommand.add_onboarding_settings(lunch_onboarding=True)

def on_message(message):
	if message == "OK":
		PiecesSettings.health = message
		PiecesSettings.is_loaded = True
	else:
		PiecesSettings.is_loaded = False
		print("Please make sure Pieces OS is running\n")

def on_close(ws):
	PiecesSettings.is_loaded = False

def plugin_loaded():
	settings = PiecesSettings.get_settings()
	host = settings.get("host")
	
	PiecesSettings.host_init(host) # Intilize the hosts url
	# callbacks needed onchange settings
	PiecesSettings.on_model_change_callbacks.append(copilot.update_status_bar)
	health = PiecesSettings.api_client.health
	if PiecesSettings.get_settings().get("auto_start_pieces_os") and not health:
			health = PiecesSettings.api_client.open_pieces_os()

	if health:
		HealthWS(PiecesSettings.api_client, on_message, startup, on_close).start()
	else:
		print("Couldn't start pieces OS\nPlease run Pieces OS and restart the editor to ensure everything is running properly")
		BaseWebsocket.close_all()


def plugin_unloaded():
	BaseWebsocket.close_all()


	
