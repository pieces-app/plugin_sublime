import sublime_plugin
import sublime

from ..settings import PiecesSettings
from ..startup_utils import check_pieces_os
from .auth_user import AuthUser


class PiecesLoginCommand(sublime_plugin.WindowCommand):
	@check_pieces_os()
	def run(self):
		sublime.set_timeout_async(lambda:PiecesSettings.api_client.user.login(True)) # Lets connect to cloud after login
		
		
class PiecesLogoutCommand(sublime_plugin.WindowCommand):
	@check_pieces_os()
	def run(self):
		sublime.set_timeout_async(lambda:PiecesSettings.api_client.user.logout())

class PiecesAllocationConnectCommand(sublime_plugin.WindowCommand):
	@check_pieces_os()
	def run(self):
		sublime.set_timeout_async(lambda:PiecesSettings.api_client.user.connect())

	def is_enabled(self):
		return bool(AuthUser.user_profile) and not bool(AuthUser.user_profile.allocation)

class PiecesAllocationDisconnectCommand(sublime_plugin.WindowCommand):
	@check_pieces_os()
	def run(self):
		sublime.set_timeout_async(lambda:PiecesSettings.api_client.user.disconnect())

	def is_enabled(self):
		return bool(AuthUser.user_profile) and bool(AuthUser.user_profile.allocation)

