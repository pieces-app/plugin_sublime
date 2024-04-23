from pieces import __version__
from pieces.api import get_application,open_pieces_os


def plugin_loaded():
    global application
    if not pieces_version:
        return print("Couldn't start pieces os")

    application = get_application()
    # USER = get_user()
    # USER_IMAGE_URL = USER.picture
    print(f"Pieces os version: {pieces_version}\nPlugin version: {__version__}")
    



