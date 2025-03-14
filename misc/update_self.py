import urllib.request
import json
import sublime_plugin
import sublime
import os
from .._pieces_lib.pieces_os_client.wrapper.version_compatibility import VersionChecker
from .._pieces_lib.pieces_os_client.wrapper.installation import PosInstaller,  DownloadModel, DownloadState

from .._version import __version__
from ..settings import PiecesSettings
from ..progress_bar import ProgressBar

SUBLIME_PACKAGE_URL = "https://builds.pieces.app/stages/production/plugin_sublime/zip/download?download=true"

class PiecesCheckSelfUpdatesCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.set_timeout_async(self.run_async)

    def run_async(self):
        try:
            latest_version = self.get_latest_tag()
            if not isinstance(latest_version, str):
                raise ValueError
        except: # Internet issues
            return

        if VersionChecker.compare(latest_version,__version__) == 1 and \
         sublime.ok_cancel_dialog(
            msg="There is a new Pieces for Sublime version, Do you want to install it?",
                ok_title="Install", title="Pieces for Sublime update"):
            self.progress_bar = ProgressBar("Installation Pieces for Sublime Plugin", total=100)
            self.progress_bar.start()
            PosInstaller(self.on_update, "").install_using_web(
                PiecesSettings.add_params(SUBLIME_PACKAGE_URL), 
                os.path.join(sublime.installed_packages_path(), "Pieces.sublime-package")
            )


    def on_update(self, model: DownloadModel):
        if model.state in [DownloadState.DOWNLOADING, DownloadState.COMPLETED]:
            self.progress_bar.update_progress(model.percent)
        elif model.state == DownloadState.FAILED:
            self.progress_bar.stop("Failed to install Pieces for Sublime")
        if model.state == DownloadState.COMPLETED:
            sublime.message_dialog("Pieces for Sublime is Updated! Please restart Sublime")


    @staticmethod
    def get_latest_tag():
        with urllib.request.urlopen("https://api.github.com/repos/pieces-app/plugin_sublime/tags") as response:
            if response.status == 200:
                data = response.read()
                tags = json.loads(data)

                if tags:
                    return tags[0]['name']