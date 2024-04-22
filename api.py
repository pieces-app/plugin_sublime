from typing import Optional
import sublime
from pieces import __version__
from pieces.config import pos_client
from pieces import config

application = None

def get_version() -> Optional[str]:
    """Get pieces os version return None if there is a problem"""
    try:
        version = pos_client.WellKnownApi(config.api_client).get_well_known_version()
        return version
    except: # There is a problem in the startup
        return None


def get_health():
    try:
        health = pos_client.WellKnownApi(config.api_client).get_well_known_version()
        return health
    except: # There is a problem in the startup
        return False


def open_pieces_os() -> Optional[str]:
    """Open pieces os and return its version"""
    version = get_version()
    if version:
        return version
    else:
    	# sublime.platform() ->  Literal['osx', 'linux', 'windows']
        pl = sublime.platform().upper()
        if pl == "windows":
            subprocess.Popen(["start", "os_server"], shell=True)
        elif pl == "linux":
            subprocess.Popen(["os_server"])
        elif pl == "osx":
            subprocess.Popen(["open", "os_server"])
        time.sleep(2) # wait for the server to open
        
        return get_version() # pieces os version

def get_application() -> pos_client.Application:
    # Decide if it's Windows, Mac, Linux or Web
    global application
    if application:
        return application
    api_instance = pos_client.ConnectorApi(config.api_client)
    seeded_connector_connection = pos_client.SeededConnectorConnection(
        application=pos_client.SeededTrackedApplication(
            name = "SUBLIME",
            platform = sublime.platform().upper() if sublime.platform() != 'osx' else "MACOS",
            version = __version__))
    api_response = api_instance.connect(seeded_connector_connection=seeded_connector_connection)
    return api_response.application


def get_user():
    api_instance = pos_client.UserApi(config.api_client)
    user = api_instance.user_snapshot().user
    return user