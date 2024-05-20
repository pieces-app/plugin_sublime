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
	"""
	Retrieves the health status from the WellKnownApi and returns True if the health is 'ok', otherwise returns False.

	Returns:
	bool: True if the health status is 'ok', False otherwise.
	"""
	try:
		health = pos_client.WellKnownApi(PiecesSettings.api_client).get_well_known_health()
		return health == "ok"
	except Exception as e:
		return False




def open_pieces_os() -> Optional[str]:
	"""Open pieces os and return its version"""
	version = get_version()
	if version:
		return version
	else:
		# sublime.platform() ->  Literal['osx', 'linux', 'windows']
		pl = sublime.platform().lower()
		if pl == "windows":
			subprocess.run(["start", "pieces://launch"], shell=True)
		elif pl == "osx":
			subprocess.run(["open","pieces://launch"])
		elif pl == "linux":
			subprocess.run(["xdg-open","pieces://launch"])

		for _ in range(2):
			version = get_version()
			if version:
				return version
			time.sleep(2) # wait for the server to open
		return get_version() # pieces os version


def get_user():
	api_instance = pos_client.UserApi(PiecesSettings.api_client)
	user = api_instance.user_snapshot().user
	return user