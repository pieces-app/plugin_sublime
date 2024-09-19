import sublime_plugin
import sublime

from ..settings import PiecesSettings
from .auth_user import AuthUser


class PiecesLoginCommand(sublime_plugin.WindowCommand):
	def run(self):
		sublime.set_timeout_async(lambda:PiecesSettings.api_client.user.login(False))

	def is_enabled(self):
		return PiecesSettings.is_loaded
		
		
class PiecesLogoutCommand(sublime_plugin.WindowCommand):
	def run(self):
		sublime.set_timeout_async(lambda:PiecesSettings.api_client.user.logout())

	def is_enabled(self):
		return PiecesSettings.is_loaded

class PiecesAllocationConnectCommand(sublime_plugin.WindowCommand):
	def run(self):
		sublime.set_timeout_async(lambda:PiecesSettings.api_client.user.connect())

	def is_enabled(self):
		return PiecesSettings.is_loaded and bool(AuthUser.user_profile) and not bool(AuthUser.user_profile.allocation)

class PiecesAllocationDisconnectCommand(sublime_plugin.WindowCommand):
	def run(self):
		sublime.set_timeout_async(lambda:PiecesSettings.api_client.user.disconnect())

	def is_enabled(self):
		return PiecesSettings.is_loaded and bool(AuthUser.user_profile) and bool(AuthUser.user_profile.allocation)

