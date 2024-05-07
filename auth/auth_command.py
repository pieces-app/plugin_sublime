import sublime_plugin

from pieces.settings import PiecesSettings
from pieces_os_client import OSApi


class PiecesLoginCommand(sublime_plugin.WindowCommand):
	def run(self):
		OSApi(PiecesSettings.api_client).sign_into_os(async_req=True)


class PiecesLogoutCommand(sublime_plugin.WindowCommand):
	def run(self):
		OSApi(PiecesSettings.api_client).sign_out_of_os(async_req=True)




