from typing import Optional
import sublime
import pieces_os_client as pos_client
from .settings import PiecesSettings
import time
import subprocess
from . import __version__
import semver


PIECES_OS_MIN_VERSION = "9.0.0"  # Minium version (9.0.0)
PIECES_OS_MAX_VERSION = "10.0.0" # Maxium version (10.0.0)

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
		print("Please update your Pieces Sublime Package is up-to-date. It is not compatible with the current Pieces OS version")
		print()
		print_version_details(pieces_os_version, __version__)
		return False
	elif os_version_parsed < min_version_parsed:
		print("Please update your Pieces OS. It is not compatible with the current package version")
		print()
		print_version_details(pieces_os_version, __version__)
		return False
	return True

def print_version_details(pieces_os_version, __version__):
	print(f"Pieces os version: {pieces_os_version}\nPlugin version: {__version__}")
