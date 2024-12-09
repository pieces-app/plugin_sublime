import sublime_plugin
from ..settings import PiecesSettings
import webbrowser
import os

class PiecesInstallPiecesOsCommand(sublime_plugin.WindowCommand):
	def run(self):

		if PiecesSettings.api_client.local_os == "WINDOWS":
			webbrowser.open(f"https://builds.pieces.app/stages/production/appinstaller/os_server.appinstaller?product={PiecesSettings.api_client.tracked_application.name.value}&download=true")

		elif PiecesSettings.api_client.local_os == "LINUX":
			webbrowser.open("https://snapcraft.io/pieces-os")
			return
		
		elif PiecesSettings.api_client.local_os == "MACOS":
			arch = os.uname().machine
			pkg_url = (
				"https://builds.pieces.app/stages/production/macos_packaging/pkg-pos-launch-only"
				f"{'-arm64' if arch == 'arm64' else ''}/download?product={PiecesSettings.api_client.tracked_application.name.value}&download=true"
			)
			webbrowser.open(pkg_url)

		else:
			raise ValueError("Invalid platform")
