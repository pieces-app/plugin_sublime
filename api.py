from typing import Optional
import sublime
from ._pieces_lib import pieces_os_client as pos_client
from .settings import PiecesSettings
import time
import subprocess
from . import __version__
from ._pieces_lib import semver

PIECES_OS_MIN_VERSION = "10.0.3"  # Minimum version (10.0.3)
PIECES_OS_MAX_VERSION = "11.0.0" # Maximum version (11.0.0)

def get_version() -> Optional[str]:
	"""Get pieces os version return None if there is a problem"""
	try:
		version = pos_client.WellKnownApi(PiecesSettings.api_client).get_well_known_version()
		return version
	except: # There is a problem in the startup
		return None




def open_pieces_os() -> Optional[str]:
	"""Open pieces os and return its version"""
	version = get_version()
	if version:
		return version
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

def version_check():
	"""Check the version of the pieces os in the within range"""
	pieces_os_version = get_version()

	# Parse version numbers
	os_version_parsed = semver.VersionInfo.parse(pieces_os_version)
	min_version_parsed = semver.VersionInfo.parse(PIECES_OS_MIN_VERSION)
	max_version_parsed = semver.VersionInfo.parse(PIECES_OS_MAX_VERSION)

	# Check compatibility
	if os_version_parsed >= max_version_parsed:
		message = "Please make sure your Pieces Sublime Package is up-to-date. It is not compatible with the current Pieces OS version"
		print()
		print()
		print_version_details(pieces_os_version, __version__)
		sublime.message_dialog(message)
		return False,"the Pieces Sublime Package"
	elif os_version_parsed < min_version_parsed:
		message = "Please make sure your Pieces OS is up-to-date. It is not compatible with the current Pieces package"
		print(message)
		print()
		print_version_details(pieces_os_version, __version__)
		sublime.message_dialog(message)
		return False,"Pieces OS"
	return True,None

def print_version_details(pieces_os_version, __version__):
	print(f"Pieces OS version: {pieces_os_version}\nPlugin version: {__version__}")
