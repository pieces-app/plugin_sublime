from . import __version__
from .settings import PiecesSettings
from .copilot.ask_command import copilot
import sublime
from ._pieces_lib.pieces_os_client.wrapper.version_compatibility import UpdateEnum
from ._pieces_lib.pieces_os_client.wrapper.websockets import (
	BaseWebsocket,
	AuthWS,HealthWS,
	ConversationWS,
	AssetsIdentifiersWS,
	AnchorsIdentifiersWS,
	LTMVisionWS,
	RangesIdentifiersWS)


from .startup_utils import check_compatiblity

# load the commands
from .assets import *
from .ask import *
from .auth import *
from .search import *
from .misc import *
from .copilot import *


def startup():
	version_check = check_compatiblity()
	if not version_check.compatible:
		plugin_name = "PiecesOS" if version_check.update == UpdateEnum.PiecesOS else "Pieces for Sublime"
		print(f"'{plugin_name}' is out of date. Please update to the latest version to ensure full functionality.")
		BaseWebsocket.close_all()
		return
	
	print(f"PiecesOS version: {PiecesSettings.api_client.version}\nPlugin version: {__version__}")
	PiecesSettings.models_init(PiecesSettings.get_settings().get('model')) # Intilize the models
	ConversationWS(PiecesSettings.api_client)
	AssetsIdentifiersWS(PiecesSettings.api_client)
	AuthWS(PiecesSettings.api_client,PiecesSettings.api_client.user.on_user_callback)
	AnchorsIdentifiersWS(PiecesSettings.api_client)
	LTMVisionWS(PiecesSettings.api_client,lambda x : None)
	RangesIdentifiersWS(PiecesSettings.api_client)
	BaseWebsocket.start_all()


	# Lunch Onboarding if it is the first time
	if not PiecesOnboardingCommand.get_onboarding_settings().get("lunch_onboarding",False):
		sublime.active_window().run_command("pieces_onboarding")
		PiecesOnboardingCommand.add_onboarding_settings(lunch_onboarding=True)



def plugin_loaded():
	# Use the auth callback instead of the default one in the client
	PiecesSettings.api_client.user.on_user_callback = AuthUser.on_user_callback 
	sublime.set_timeout_async(run_async)
	

def run_async():
	# callbacks needed onchange settings
	PiecesSettings.on_model_change_callbacks.append(copilot.update_status_bar)
	health = PiecesSettings.api_client.is_pieces_running()
	if PiecesSettings.get_settings().get("auto_start_pieces_os"):
		health = PiecesSettings.api_client.open_pieces_os()
	health_ws = HealthWS(PiecesSettings.api_client, lambda x:startup())
	if health:
		health_ws.start()
	else:
		print("Please make sure PiecesOS is running")
		BaseWebsocket.close_all()


def plugin_unloaded():
	BaseWebsocket.close_all()


