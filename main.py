from . import __version__
from .api import open_pieces_os,print_version_details,version_check
from .settings import PiecesSettings

import sublime

# load the commands
from .assets import *
from .ask import *
from .auth import *
from .search import *
from .misc import *
from .base_websocket import BaseWebsocket

PiecesSettings.host_init() # Intilize the hosts url

def startup():
	pieces_version = open_pieces_os()


	if not pieces_version:
		print("Couldn't start pieces os\nPlease run pieces os and restart the editor to ensure everything is running properly")
	else:
		if version_check()[0]:
			PiecesSettings.is_loaded = True
			PiecesSettings.models_init()  # initilize the models
			PiecesSettings.get_application()
			print_version_details(pieces_version, __version__)


	# Preferences settings
	preferences_settings = sublime.load_settings('Preferences.sublime-settings')
	preferences_settings.add_on_change("PREFERENCES_SETTINGS",ColorSchemeGenerator.generate_color_scheme)
	ColorSchemeGenerator.generate_color_scheme()

	# WEBSOCKETS:
	# Assets Identifiers Websocket
	AssetsIdentifiersWS(AssetSnapshot.assets_snapshot_callback).start() # Load the assets ws at the startup
	
	# User Weboscket
	PiecesSettings.create_auth_output_panel()
	AuthWebsocket(AuthUser.on_user_callback).start() # Load the stream user websocket		

def plugin_loaded():
	sublime.set_timeout_async(startup,0)
	

def plugin_unloaded():
	BaseWebsocket.close_all()


	
