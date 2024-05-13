from pieces_os_client import UserProfile,AllocationsApi
from pieces.settings import PiecesSettings
import sublime

class AuthUser:
	output_panel = None
	phantom_set = None
	connect = False # should we connect to the allocation server

	@classmethod
	def on_user_callback(cls,user:UserProfile=None):
		
		if not user:
			cls.login_page()
		else:
			cls.logout_page(user.email,user.name,user.allocation)
			if cls.connect:
				AllocationsApi(PiecesSettings.api_client).allocations_connect_new_cloud(user)
				cls.connect = False # Rest the connect variable



	@classmethod
	def login_page(cls):
		cls.phantom_set.update([])
		phantom_content = '<a href="subl:pieces_login"><b>Connect to your account</b></a>'
		phantom = sublime.Phantom(sublime.Region(0, 500), phantom_content, sublime.LAYOUT_INLINE)
		cls.phantom_set.update([phantom])

	@classmethod
	def logout_page(cls,email,username,allocation):
		if allocation:
			allocation_html = f"<p>Cloud Status: <span style=color:green>•</span> Connected</p>"
			try:
				if allocation.urls.vanity.url:
					allocation_html += f"<p>Personal Domain: {allocation.urls.vanity.url}</p>"
			except AttributeError:
				pass
		else:
			if cls.connect:
				allocation_html = "<p>Cloud Status: <span style=color:yellow>•</span> Connecting</p>"
			else:
				allocation_html = "<p>Cloud Status: <span style=color:red>•</span> Disconnected</p>"
		
		cls.phantom_set.update([])
		phantom_content = f"<p>Username: {username}</p><p>Email: {email}</p>{allocation_html}<a href='subl:pieces_logout'>Logout</a>"
		phantom = sublime.Phantom(sublime.Region(0, 500), phantom_content, sublime.LAYOUT_INLINE)
		cls.phantom_set.update([phantom])
