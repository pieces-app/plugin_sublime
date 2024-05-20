from pieces_os_client import UserProfile
from pieces.settings import PiecesSettings
import sublime


CONNECTING_HTML = "<p>Cloud Status: <span style=color:yellow>•</span> Connecting</p>"
DISCONNECTED_HTML = "<p>Cloud Status: <span style=color:red>•</span> Disconnected</p>"
CONNECTED_HTML = "<p>Cloud Status: <span style=color:green>•</span> Connected</p>"


class AuthUser:
	phantom_set = None
	user_profile = None # Cache the user


	@classmethod
	def get_phantom_set(cls):
		if cls.phantom_set:
			return cls.phantom_set
		cls.phantom_set = sublime.PhantomSet(PiecesSettings.output_panel, "pieces_auth")
		return cls.phantom_set

	@classmethod
	def on_user_callback(cls,user:UserProfile=None):
		phantom_set = cls.get_phantom_set()
		phantom_set.update([]) # Clear the output panel
		sublime.active_window().focus_view(PiecesSettings.output_panel)
		cls.user_profile = user
		if not user:
			cls.login_page()
		else:
			cls.logout_page(user.email,user.name,user.allocation)

	@classmethod
	def login_page(cls):
		phantom_set = cls.get_phantom_set()
		phantom_content = '<a href="subl:pieces_login"><b>Connect to your account</b></a>'
		phantom = sublime.Phantom(sublime.Region(0, 500), phantom_content, sublime.LAYOUT_INLINE)
		phantom_set.update([phantom])

	@classmethod
	def logout_page(cls,email,username,allocation=None,connecting=False):
		phantom_set = cls.get_phantom_set()
		if allocation:
			allocation_html = ""
			status = allocation.status.cloud
			if status == "PENDING":
				allocation_html = CONNECTING_HTML
			elif status == "RUNNING" and "SUCCEEDED":
				allocation_html = CONNECTED_HTML
			elif status == "FAILED":
				allocation_html = DISCONNECTED_HTML

			try:
				if allocation.urls.vanity.url:
					allocation_html += f"<p>Personal Domain: {allocation.urls.vanity.url}</p>"
			except AttributeError:
				pass
		else:
			if connecting:
				allocation_html = CONNECTING_HTML
			else:
				allocation_html = DISCONNECTED_HTML
		phantom_content = f"<p>Username: {username}</p><p>Email: {email}</p>{allocation_html}<a href='subl:pieces_logout'>Logout</a>"
		phantom = sublime.Phantom(sublime.Region(0, 500), phantom_content, sublime.LAYOUT_INLINE)
		phantom_set.update([phantom])
