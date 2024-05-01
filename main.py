from pieces import __version__
from pieces.api import open_pieces_os
from pieces.settings import PiecesSettings

import sublime

# load the commands
from pieces.assets import *
from pieces.ask import *


def startup():
	pieces_version = open_pieces_os()

	if not pieces_version:
		return print("Couldn't start pieces os")

	# USER = get_user()
	# USER_IMAGE_URL = USER.picture

	print(f"Pieces os version: {pieces_version}\nPlugin version: {__version__}")

	settings = sublime.load_settings('pieces.sublime-settings')

	settings.add_on_change("PIECES_SETTINGS",PiecesSettings.on_settings_change)



def plugin_loaded():
	PiecesSettings.on_settings_change()  # Run the settings
	sublime.set_timeout_async(startup,0)
	AssetsIdentifiersWS(AssetSnapshot.assets_snapshot_callback) # Load the assets ws at the startup
	

	
