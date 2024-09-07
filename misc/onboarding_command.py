from typing import List
import sublime_plugin
import sublime
import time
import os
import json

from ..settings import PiecesSettings

CSS = """
html.dark {
	--pieces-forground: color(var(--forground) blend(white 95%));
	--pieces-h1: color(var(--greenish) blend(white 90%));
}
html.light {
	--pieces-forground: color(var(--forground) blend(black 95%));
	--pieces-h1: color(var(--greenish) blend(black 90%));
}
.container {
	padding: 20px;
}
h1 {
	color: var(--pieces-h1);
}
p {
	font-size: 14px;
}
ul {
	list-style-type: disc;
	margin-left: 20px;
}
.step {
	margin-bottom: 15px;
}
.step-title {
	font-weight: bold;
	color: var(--pieces-forground);
}
.step-description {
	margin-left: 20px;
}
"""

html_template = """
<body>
	<style>
		{css}
	</style>
	<div class="container">
		<h1>Welcome to Pieces for Developers!</h1>
		<p>Follow these steps to get started:</p>
		<div class="step">
			<div class="step-title">Step 1: Pieces OS Installation</div>
			<div class="step-description">
				{os_status}
			</div>
		</div>
		<div class="step">
			<div class="step-title">Step 2: Create your first Snippet</div>
			<div class="step-description">
				{create_status}
			</div>
		</div>
		<div class="step">
			<div class="step-title">Step 3: View your saved snippets</div>
			<div class="step-description">
				{open_status}
			</div>
		</div>
		<div class="step">
			<div class="step-title">Step 4: Search for your saved snippet</div>
			<div class="step-description">
				{search_status}
			</div>
		</div>
		<div class="step">
			<div class="step-title">Step 5: Ask for help</div>
			<div class="step-description">
				{ask_status}
			</div>
		</div>
		<div class="step">
			<div class="step-title">Step 6: Pieces Copilot</div>
			<div class="step-description">
				{copilot_status}
			</div>
		</div>
		<div class="step">
			<div class="step-title">Step 7: Explain</div>
			<div class="step-description">
				{explain_status}
			</div>
		</div>
		<div class="step">
			<div class="step-title">Step 8: Explore the Features</div>
			<div class="step-description">
				Check out the <a href="https://example.com/docs">documentation</a> to learn about all the features and how to use them effectively.
			</div>
		</div>
		<div class="step">
			<div class="step-title">Step 9: Get Support</div>
			<div class="step-description">
				Feeling stuck or encountering bugs? No worries! Head over to your command palette and select <code><a href="subl:pieces_support">Pieces: Get Support</a></code>. You'll discover a treasure trove of useful resources to help you out!
			</div>
		</div>
		<div class="step">
			<div class="step-title">Step 10: Join the Community</div>
			<div class="step-description">
				Don't forget to join our <a href="https://docs.pieces.app/community/">community</a><br>
				Don't forget also to check the <a href="subl:pieces_about">Pieces: About</a> command for your command palette.
			</div>
		</div>
		<p>Enjoy using the Package! :)</p>
		<a href="subl:pieces_onboarding">Reload the view</a>
		<a href="subl:pieces_reset_onboarding">Reset Onboarding</a>
	</div>
</body>
"""	
def green(text:str) -> str:
	return f'<span style="color:var(--greenish)">{text}</span>'

def red(text:str) -> str:
	return f'<span style="color:var(--redish)">{text}</span>'

def subl_onboarding_commands(title,cmd):	
	return f"""<a href='subl:{sublime.html_format_command("pieces_onboarding_commands",args={"cmd":cmd})}'>{title}</a>"""

class PiecesOnboardingCommand(sublime_plugin.WindowCommand):
	SHEET_NAME = "Welcome to Pieces 🎉🎉!"
	calls = {}
	clearing_time = time.time()
	sheet_id = None

	lazy_load_status = {
		"pieces_os_status":"Checking Pieces OS",
	} # Maps a function name to the status to be displayed when it is loading

	ONBOARDING_SETTINGS_PATH = os.path.join(PiecesSettings.PIECES_USER_DIRECTORY, "onboarding_settings.json")
	
	def run(self):
		sheet = sublime.HtmlSheet(self.sheet_id) if self.sheet_id in self.get_html_sheet_ids() else self.window.new_html_sheet(self.SHEET_NAME,"") 
		self.sheet_id = sheet.id()
		self.reload(sheet)

	def is_enabled(self) -> bool:
		return PiecesSettings.is_loaded

	@staticmethod
	def get_html_sheet_ids() -> List[int]:
		ids = []
		for window in sublime.windows():
			for sheet in window.sheets():
				if isinstance(sheet,sublime.HtmlSheet):
					ids.append(sheet.id())
		return ids

	def reload(self,sheet):
		kwargs = {
			"os_status":self.pieces_os_status(),
			"create_status":self.create_command_status(),
			"open_status":self.open_asset_command_status(),
			"search_status":self.search_command_status(),
			"ask_status":self.ask_question_command_status(),
			"copilot_status":self.copilot_status(),
			"explain_status":self.explain_status(),
			"css":CSS,
		}
		sheet.set_contents(html_template.format(**kwargs))


	def pieces_os_status(self):
		if PiecesSettings.api_client.is_pieces_running:
			return green('Installed Pieces OS is installed successfully')
		return red("Oops! Pieces OS is not running.") + """
			<br>
			Don't worry, you can easily <a href="subl:pieces_open_pieces">open Pieces OS</a> and get started right away!<br>
			Curious to learn more? <a href="https://docs.pieces.app/installation-getting-started/pieces-os">Click here</a> to explore the full documentation and discover all the amazing features of Pieces OS.
		"""

	def create_command_status(self):
		settings = self.get_onboarding_settings()
		if settings.get("create"):
			return green('Congratulations on creating your first snippet! Keep exploring and creating more to enhance your coding experience')
		return f"""Snippets {subl_onboarding_commands("creation","create")} are like little treasures of code! Save them, and you'll have a goldmine of solutions. Plus, with a quick search, you can uncover exactly what you need in no time!"""

	def open_asset_command_status(self):
		settings = self.get_onboarding_settings()
		if settings.get("open"):
			return green('Great job! You viewed your saved snippet.')
		return '<a href="subl:pieces_list_assets">Click here</a> to explore all your snippets and keep the creativity flowing!'

	def ask_question_command_status(self):
		settings = self.get_onboarding_settings()
		if settings.get("ask"):
			return green('Bug solved! Great job!')
		return subl_onboarding_commands("Ask for help and get those bugs fixed!",'ask')
	
	def search_command_status(self):
		settings = self.get_onboarding_settings()
		if settings.get("search"):
			return green('Seached for snippet successfully!')
		return """Ever lost your code snippet and spent hours searching for it? Discover our cutting-edge <a href="subl:pieces_search">searching</a> technology that makes finding your snippets a breeze!"""


	def copilot_status(self):
		settings = self.get_onboarding_settings()
		if settings.get("copilot"):
			return green('Chatted with the copilot successfully!')
		return """Looking for your personal Assistant? Ask it any question! Open the <a href="subl:pieces_ask_stream">Copilot</a> and dive into an exciting conversation with it. Discover the possibilities!"""

	def share_status(self):
		settings = self.get_onboarding_settings()
		if settings.get("share"):
			return green("Shared your Snippet successfully")
		return f"{subl_onboarding_commands('Generate a shareable link','share')} to share it with others"
	
	def explain_status(self):
		settings= self.get_onboarding_settings()
		if settings.get("explain"):
			return green("You asked for the Copilot explanation")
		return f'Want help with a code block that you can\'t understand? Ask Pieces for code {subl_onboarding_commands("explanation","explain")}'

	@classmethod
	def get_onboarding_settings(cls):
		if not os.path.exists(cls.ONBOARDING_SETTINGS_PATH):
			return {}
		with open(cls.ONBOARDING_SETTINGS_PATH,"r") as f:
			return json.load(f)
	
	@classmethod
	def add_onboarding_settings(cls, **kwargs):
		# Load existing settings
		data = cls.get_onboarding_settings()
		
		# Update the settings with the new kwargs
		data.update(kwargs)
		
		with open(cls.ONBOARDING_SETTINGS_PATH, "w") as f:
			json.dump(data, f, indent=4)
		if cls.sheet_id in cls.get_html_sheet_ids():
			sublime.active_window().run_command("pieces_onboarding") # Reload the onboarding command



snippet_create = """
# Gettings string size in bytes!
str1 = "hello"
str2 = "?"

def str_size(s):
  return len(s.encode('utf-8'))

str_size(str1)
str_size(str2)
"""

snippet_ask = """
def is_palindrome(s):
	return s == s[-1]

print(is_palindrome("A man a plan a canal Panama"))
"""
class PiecesOnboardingCommandsCommand(sublime_plugin.WindowCommand):
	def run(self,cmd):
		if cmd == "create":
			self.create_onboarding_view(snippet_create,
				"Create your first asset 🆕",
				"Right click to open your context menu Then go to 'Pieces > Save to Pieces'"
				)
		elif cmd == "ask":
			self.create_onboarding_view(snippet_ask,
				"Ask for bug fix 🤔",
				"Right click to open your context menu Then go to 'Pieces > Ask Copilot > Fix Bug'"
				)
		elif cmd == "share":
			self.create_onboarding_view(snippet_create,
				"Share a Snippet ✉",
				"Right click to open your context menu Then go to 'Pieces > Generate Shareable Link'"
				)
		elif cmd == "explain":
			self.create_onboarding_view(snippet_create,"Explain.py","Right click to open your context menu Then go to 'Pieces > Explain'")

	def create_onboarding_view(self,snippet,name,popup_text):
		new_file = self.window.new_file(syntax="Packages/Python/Python.sublime-syntax")
		new_file.run_command("append",{"characters":snippet})
		new_file.run_command("select_all")
		new_file.set_name(name)
		new_file.set_scratch(True)
		new_file.show_popup(popup_text)

class PiecesResetOnboardingCommand(sublime_plugin.WindowCommand):
	def run(self):
		if sublime.yes_no_cancel_dialog("Are you sure you want to reset your onboarding progress"):
			os.remove(PiecesOnboardingCommand.ONBOARDING_SETTINGS_PATH)
			self.window.run_command("pieces_onboarding")
