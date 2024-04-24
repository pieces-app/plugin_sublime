from pieces import __version__
from pieces.api import get_application,open_pieces_os
from pieces.config import on_settings_change

import sublime

# load the commands
from pieces.assets import *


def startup():
    
    pieces_version = open_pieces_os()

    if not pieces_version:
        return print("Couldn't start pieces os")
    
    get_application() # Update the application
    
    # USER = get_user()
    # USER_IMAGE_URL = USER.picture
    print(f"Pieces os version: {pieces_version}\nPlugin version: {__version__}")

def plugin_loaded():
    on_settings_change()  # Run the settings
    sublime.set_timeout_async(startup,0)
    AssetsIdentifiersWS(assets_snapshot_callback) # Load the assets ws at the startup

    
