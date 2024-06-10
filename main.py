from . import __version__
from .api import open_pieces_os,print_version_details,version_check
from .settings import PiecesSettings

import sublime
import asyncio

# load the commands
from .assets import *
from .ask import *
from .auth import *
from .search import *
from .misc import *
from .copilot import *
from .base_websocket import BaseWebsocket

PiecesSettings.host_init() # Intilize the hosts url

def startup():
	pieces_version = open_pieces_os()


	if not pieces_version:
		print("Couldn't start pieces os\nPlease run pieces os and restart the editor to ensure everything is running properly")
	else:
		if version_check():
			PiecesSettings.is_loaded = True
			PiecesSettings.models_init()  # initilize the models
			PiecesSettings.get_application()
			print_version_details(pieces_version, __version__)


	settings = sublime.load_settings('Pieces.sublime-settings')

	settings.add_on_change("PIECES_SETTINGS",PiecesSettings.on_settings_change)
	
	

	# WEBSOCKETS:
	# Assets Identifiers Websocket
	AssetsIdentifiersWS(AssetSnapshot.assets_snapshot_callback).start() # Load the assets ws at the startup
	
	# User Weboscket
	PiecesSettings.create_auth_output_panel()
	AuthWebsocket(AuthUser.on_user_callback).start() # Load the stream user websocket

	# Ask Stream Websocket
	AskStreamWS(PiecesAskStreamCommand.on_message_callback).start()


def plugin_loaded():
	sublime.set_timeout_async(startup,0)
	

def plugin_unloaded():
	BaseWebsocket.close_all()


	
