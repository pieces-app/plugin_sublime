import sublime_plugin
from ..settings import PiecesSettings
import webbrowser
import os
from .._pieces_lib.pieces_os_client.wrapper.installation import DownloadModel, DownloadState
from ..progress_bar import ProgressBar

lock = False

class PiecesInstallPiecesOsCommand(sublime_plugin.WindowCommand):
	def run(self):
		global lock
		if lock == True:
			return
		lock = True
		self.progress_bar = ProgressBar("Installation PiecesOS", total=100)
		PiecesSettings.api_client.pieces_os_installer(self.on_update).start_download()
		self.progress_bar.start()

	def on_update(self, model: DownloadModel):
		global lock
		if model.state == DownloadState.DOWNLOADING:
			self.progress_bar.update_progress(model.percent)
		elif model.state == DownloadState.COMPLETED:
			self.progress_bar.update_progress(100)
			lock = False
		elif model.state == DownloadState.FAILED:
			self.progress_bar.stop("Failed to install Pieces")
			self.download_docs()
			lock = False

	def download_docs(self):
		if PiecesSettings.api_client.local_os == "WINDOWS":
			webbrowser.open(f"https://builds.pieces.app/stages/production/appinstaller/os_server.appinstaller?product=SUBLIME&download=true")

		elif PiecesSettings.api_client.local_os == "LINUX":
			webbrowser.open("https://snapcraft.io/pieces-os")
			return
		
		elif PiecesSettings.api_client.local_os == "MACOS":
			arch = os.uname().machine
			pkg_url = (
				"https://builds.pieces.app/stages/production/macos_packaging/pkg-pos-launch-only"
				f"{'-arm64' if arch == 'arm64' else ''}/download?product=SUBLIME&download=true"
			)
			webbrowser.open(pkg_url)

		else:
			raise ValueError("Invalid platform")