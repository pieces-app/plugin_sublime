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
	AssetsIdentifiersWS(AssetSnapshot.assets_snapshot_callback) # Load the assets ws at the startup
	
	# User Weboscket
	PiecesSettings.create_auth_output_panel()
	AuthWebsocket(AuthUser.on_user_callback) # Load the stream user websocket

def plugin_loaded():
	PiecesSettings.host_init() # Intilize the hosts url
	sublime.set_timeout_async(startup,0)
	

def plugin_unloaded():
	asyncio.run(AssetsIdentifiersWS().close_websocket_connection())
	asyncio.run(AuthWebsocket().close_websocket_connection())


	
