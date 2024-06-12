from . import __version__
from .api import open_pieces_os,print_version_details,version_check
from .settings import PiecesSettings
from .copilot.ask_command import copilot
import sublime

# load the commands
from .assets import *
from .ask import *
from .auth import *
from .search import *
from .misc import *
from .copilot import *
from .base_websocket import BaseWebsocket



def startup(settings_model):
	pieces_version = open_pieces_os()


	if not pieces_version:
		print("Couldn't start pieces os\nPlease run pieces os and restart the editor to ensure everything is running properly")
	else:
		if version_check():
			PiecesSettings.is_loaded = True
			PiecesSettings.get_application()
			print_version_details(pieces_version, __version__)

			
			PiecesSettings.models_init(settings_model) # Intilize the models
	

	# WEBSOCKETS:
	# Assets Identifiers Websocket
	AssetsIdentifiersWS(AssetSnapshot.streamed_identifiers_callback).start() # Load the assets ws at the startup
	
	# User Weboscket
	PiecesSettings.create_auth_output_panel()
	AuthWebsocket(AuthUser.on_user_callback).start() # Load the stream user websocket

	# Conversation Websocket
	ConversationWS(ConversationsSnapshot.streamed_identifiers_callback).start()


def plugin_loaded():
	global settings # Set it to global to use 

	settings = sublime.load_settings('Pieces.sublime-settings')
	host = settings.get("host")
	model = settings.get('model')
	settings.add_on_change("PIECES_SETTINGS",PiecesSettings.on_settings_change)
	PiecesSettings.host_init(host) # Intilize the hosts url
	
	# callbacks needed onchange settings
	PiecesSettings.on_model_change_callbacks.append(copilot.update_status_bar)

	sublime.set_timeout_async(lambda : startup(model) ,0)
	

def plugin_unloaded():
	BaseWebsocket.close_all()


	
