from ._version import __version__
from .settings import PiecesSettings
from .copilot.ask_command import PiecesConversationIdInputHandler, copilot
import sublime
from ._pieces_lib.pieces_os_client.wrapper.version_compatibility import UpdateEnum
from ._pieces_lib.pieces_os_client.wrapper.streamed_identifiers._streamed_identifiers import StreamedIdentifiersCache
from ._pieces_lib.pieces_os_client.wrapper.websockets import (
	BaseWebsocket,
	AuthWS,HealthWS,
	ConversationWS,
	AssetsIdentifiersWS,
	AnchorsIdentifiersWS,
)

from .auth.auth_user import AuthUser
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
	ConversationWS(PiecesSettings.api_client, 
		on_conversation_update=PiecesConversationIdInputHandler.cache_annotation)
	AssetsIdentifiersWS(PiecesSettings.api_client,
		on_asset_update=PiecesListAssetsCommand.on_asset_update,
		on_asset_remove=PiecesListAssetsCommand.on_asset_delete)
	AuthWS(PiecesSettings.api_client,PiecesSettings.api_client.user.on_user_callback)
	AnchorsIdentifiersWS(PiecesSettings.api_client)
	# LTMVisionWS(PiecesSettings.api_client,lambda x : None) # not super useful websocket,avoid blocking the async thread
	StreamedIdentifiersCache.pieces_client = PiecesSettings.api_client
	BaseWebsocket.start_all()
	PiecesSettings.on_settings_change()


	# Lunch Onboarding if it is the first time
	if not PiecesOnboardingCommand.get_onboarding_settings().get("lunch_onboarding",False):
		sublime.active_window().run_command("pieces_onboarding")
		PiecesOnboardingCommand.add_onboarding_settings(lunch_onboarding=True)



def plugin_loaded():
	# Load the settings from 'Pieces.sublime-settings' file using Sublime Text API
	pieces_settings = sublime.load_settings('Pieces.sublime-settings')
	pieces_settings.add_on_change("PIECES_SETTINGS",PiecesSettings.on_settings_change)

	# Use the auth callback instead of the default one in the client
	PiecesSettings.api_client.user.on_user_callback = AuthUser.on_user_callback 
	if PiecesSettings.get_settings().get("auto_check_updates", True):
		sublime.run_command("pieces_check_self_updates")
	sublime.set_timeout_async(run_async)
	

def run_async():
	# callbacks needed onchange settings
	PiecesSettings.on_model_change_callbacks.append(copilot.update_status_bar)
	health = PiecesSettings.api_client.is_pieces_running()
	if PiecesSettings.get_settings().get("auto_start_pieces_os"):
		health = PiecesSettings.api_client.open_pieces_os()
	health_ws = HealthWS(PiecesSettings.api_client,on_message_callback=lambda x:None, on_open_callback = lambda x:startup())
	if health:
		health_ws.start()
	else:
		print("Please make sure PiecesOS is running")
		BaseWebsocket.close_all()


def plugin_unloaded():
	BaseWebsocket.close_all()
	for view in copilot.gpt_clones:
		if view.is_valid:
			view.close()

