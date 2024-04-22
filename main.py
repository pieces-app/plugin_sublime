from pieces import __version__
from pieces.api import get_application,open_pieces_os,get_user
from pieces.copilot.pieces_websocket import WebSocketManager

# Load the PiecesAskStreamCommand
from pieces.copilot.pieces_ask import PiecesAskStreamCommand


def plugin_loaded():
    global application,ws_manager,USER_IMAGE_URL
    ws_manager = WebSocketManager()
    pieces_version = open_pieces_os()
    if not pieces_version:
        return print("Couldn't start pieces os")

    application = get_application()
    USER = get_user()
    USER_IMAGE_URL = USER.picture
    print(f"Pieces os version: {pieces_version}\nPlugin version: {__version__}")
    



def plugin_unload():
    if ws_manager.is_connected:
        ws_manager.close_websocket_connection()

