from pieces_os_client import UserProfile

import sublime

class AuthUser:
	output_panel = None
	phantom_set = None

	@classmethod
	def on_user_callback(cls,user:UserProfile=None):
		if not user:
			cls.login_page()
		else:
			cls.logout_page(user.email,user.name,user.allocation)

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
			if allocation.urls.vanity.url:
				allocation_html += f"<p>Personal Domain: {allocation.urls.vanity.url}</p>"
			
		else:
			allocation_html = "<p>Cloud Status: <span style=color:red>•</span> Disconnected</p>"
		cls.phantom_set.update([])
		phantom_content = f"<p>Username: {username}</p><p>Email: {email}</p>{allocation_html}<a href='subl:pieces_logout'>Logout</a>"
		phantom = sublime.Phantom(sublime.Region(0, 500), phantom_content, sublime.LAYOUT_INLINE)
		cls.phantom_set.update([phantom])
