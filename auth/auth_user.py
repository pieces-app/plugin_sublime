from .._pieces_lib.pieces_os_client import UserProfile,AllocationStatusEnum
from ..settings import PiecesSettings
import sublime
from typing import Optional


CONNECTING_HTML = "<p>Cloud Status: <span style=color:yellow>•</span> Connecting</p>"
DISCONNECTED_HTML = "<p>Cloud Status: <span style=color:red>•</span> Disconnected</p>"
CONNECTED_HTML = "<p>Cloud Status: <span style=color:green>•</span> Connected</p>"


class AuthUser:
	user_profile = None # Cache the user

	@classmethod
	def create_new_phantom(cls,html):
		PiecesSettings.output_panel.erase_phantoms("auth_phantom") # Remove the old phantom
		PiecesSettings.output_panel.add_phantom("auth_phantom", 
			sublime.Region(0, 0), html, sublime.LAYOUT_INLINE)

	@classmethod
	def on_user_callback(cls,user:Optional[UserProfile]=None,connecting=False):
		PiecesSettings.api_client.user.user_profile = user
		sublime.active_window().focus_view(PiecesSettings.output_panel)
		cls.user_profile = user
		if not user:
			cls.login_page()
		else:
			cls.logout_page(connecting)

	@classmethod
	def login_page(cls):
		phantom_content = '<a href="subl:pieces_login"><b>Connect to your account</b></a>'
		cls.create_new_phantom(phantom_content)
		

	@classmethod
	def logout_page(cls,connecting=False):
		allocation_html = ""
		user = PiecesSettings.api_client.user
		status = user.cloud_status
		if status:

			if status == AllocationStatusEnum.PENDING:
				allocation_html = CONNECTING_HTML
			elif status == AllocationStatusEnum.SUCCEEDED \
			 or status ==  AllocationStatusEnum.RUNNING:
				allocation_html = CONNECTED_HTML
			elif status == AllocationStatusEnum.FAILED:
				allocation_html = DISCONNECTED_HTML

			if user.vanity_name:
				allocation_html += f"<p>Personal Domain: {user.vanity_name}.pieces.cloud</p>"
		else:
			if connecting:
				allocation_html = CONNECTING_HTML
			else:
				allocation_html = DISCONNECTED_HTML
		phantom_content = f"<p>Username: {user.name}</p><p>Email: {user.email}</p>{allocation_html}<a href='subl:pieces_logout'>Logout</a>"
		cls.create_new_phantom(phantom_content)
