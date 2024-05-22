import sublime_plugin
import sublime

from ..settings import PiecesSettings
from .auth_user import AuthUser

from pieces_os_client import OSApi,AllocationsApi,UserApi


class PiecesLoginCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.login_thread = OSApi(PiecesSettings.api_client).sign_into_os(async_req=True)
		sublime.set_timeout_async(self.run_allocation_async)

	def run_allocation_async(self):
		try:
			user = self.login_thread.get(120) # 120 sec timeout 
			self.window.run_command("pieces_allocation_connect")
		except:
			pass

	def is_enabled(self):
		return PiecesSettings().is_loaded
		
		
class PiecesLogoutCommand(sublime_plugin.WindowCommand):
	def run(self):
		OSApi(PiecesSettings.api_client).sign_out_of_os(async_req=True)

	def is_enabled(self):
		return PiecesSettings().is_loaded

class PiecesAllocationConnectCommand(sublime_plugin.WindowCommand):
	def run(self):
		user = AuthUser.user_profile
		if user: # User logged in
			AuthUser.logout_page(user.email,user.name,None,True)
			AllocationsApi(PiecesSettings.api_client).allocations_connect_new_cloud(user,async_req=True)

	def is_enabled(self):
		return PiecesSettings().is_loaded

	def is_visible(self): # will appear if the user logged in but no allocation 
		return bool(AuthUser.user_profile) and not bool(AuthUser.user_profile.allocation)

class PiecesAllocationDisconnectCommand(sublime_plugin.WindowCommand):
	def run(self):
		if AuthUser.user_profile:
			if AuthUser.user_profile.allocation: # Check if there is an allocation iterable
				AllocationsApi(PiecesSettings.api_client).allocations_disconnect_cloud(AuthUser.user_profile.allocation,async_req=True)
	
	def is_visible(self): # will appear if the user logged in but no allocation 
		return bool(AuthUser.user_profile) and bool(AuthUser.user_profile.allocation)


	def is_enabled(self):
		return PiecesSettings().is_loaded

