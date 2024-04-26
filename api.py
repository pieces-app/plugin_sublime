from typing import Optional
import sublime
import pieces_os_client as pos_client
from pieces.settings import PiecesSettings
import time
import subprocess


def get_version() -> Optional[str]:
    """Get pieces os version return None if there is a problem"""
    try:
        version = pos_client.WellKnownApi(PiecesSettings.api_client).get_well_known_version()
        return version
    except: # There is a problem in the startup
        return None


def get_health():
    try:
        health = pos_client.WellKnownApi(PiecesSettings.api_client).get_well_known_health()
        return health == "ok"
    except: # There is a problem in the startup
        return False


def open_pieces_os() -> Optional[str]:
    """Open pieces os and return its version"""
    version = get_version()
    if version:
        return version
	# sublime.platform() ->  Literal['osx', 'linux', 'windows']
    pl = sublime.platform().lower()
    if pl == "windows":
        subprocess.Popen(["start", "os_server"], shell=True)
    elif pl == "linux":
        subprocess.Popen(["os_server"])
    elif pl == "osx":
        subprocess.Popen(["open", "os_server"])
    # Check pieces every 2 seconds if it is opened
    for _ in range(4):
        time.sleep(2) # wait for the server to open
        version = get_version()
        if version:
            return version
    return get_version() # pieces os version



def get_user():
    api_instance = pos_client.UserApi(PiecesSettings.api_client)
    user = api_instance.user_snapshot().user
    return user