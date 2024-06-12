import sublime_plugin
import sublime
import re
import time
import os
import json

from ...settings import PiecesSettings
from ...api import version_check,open_pieces_os
from ... import PiecesDependencies




class PiecesOnBoardingHandlerCommand(sublime_plugin.TextCommand):
	calls = {}
	clearing_time = time.time()

	lazy_load_status = {
		"pieces_os_status":"[Loading] Checking Pieces OS",
	} # Maps a function name to the status to be displayed when it is loading

	ONBOARDING_SETTINGS_PATH = os.path.join(PiecesSettings.PIECES_USER_DIRECTORY, "onboarding_settings.json")

	def run(self,_):
		self.reload()


	def reload(self):
		text = "\n".join(
			[self.pieces_os_status(),self.dependencies_status(),
			self.create_command_status(),self.open_asset_command_status(),self.ask_question_command_status()]
		)
		# set read only false
		self.view.set_read_only(False)
		# Erase the entire region
		self.view.run_command("select_all")
		self.view.run_command("right_delete")
		# Appending
		self.append_view(text)
		
		# Set readonly
		self.view.set_read_only(True)
		

	def _lazy_load(func):
		def wrapper(self,*args, **kwargs):
			"""
			Wrapper will be used on the function that takes time to load
			it will return a placeholder with loading utill it is loaded
			"""
			if self.clearing_time < time.time():
				self.clearing_time = time.time() + 20
				self.calls = {}

			def load_function():
				self.calls[func.__name__] = func(*args, **kwargs)
				self.reload()

			if self.calls.get(func.__name__):
				return self.calls[func.__name__] 
			else:
				sublime.set_timeout_async(load_function,0)
				return self.lazy_load_status.get(func.__name__,"[Loading]")
		return wrapper


	@_lazy_load
	def pieces_os_status():
		if PiecesSettings().get_health():
			check_version,update = version_check()
			if not check_version:
				return f'[Failed] You need to update {update}'
			return '[Success] Installed Pieces OS'
		return '[Failed] Pieces OS is not running <a href="open_pieces">open Pieces OS</a>'


	@staticmethod
	def dependencies_status():
		if PiecesDependencies.downloading:
			return "[In Progress] Downloading some dependencies"
		return "[Success] Downloaded some dependencies successfully"

	def create_command_status(self):
		settings = self.get_onboarding_settings()
		if settings.get("create_asset"):
			return '[Success] Asset created successfully!'
		return '[In Progress] Create your first<a href="create_asset">asset</a>'

	def open_asset_command_status(self):
		settings = self.get_onboarding_settings()
		if settings.get("open"):
			return '[Success] You opened an asset'
		return '[In Progress] <a href="open">Open</a>an asset'

	def ask_question_command_status(self):
		settings = self.get_onboarding_settings()
		if settings.get("ask_question"):
			return '[Success] Bug solved!'
		return '[In Progress] <a href="ask_question">Ask</a>for help and bug fixes'

	def append_view(self, text):
		"""This will replace any "a" tag by a phantom in the same place"""
		# Regular expression to find anchor tags
		anchor_pattern = re.compile(r'<a href="(.*?)">(.*?)</a>')

		phantoms = []
		new_text = ""
		last_end = 0
		offset = 0

		for match in anchor_pattern.finditer(text):
			# Extract URL and text from anchor tag
			url = match.group(1)
			anchor_text = match.group(2)

			# Create phantom HTML
			phantom_html = f'<a style="color:royalblue;" href="{url}">{anchor_text}</a>'

			# Find the start and end positions of the match in the original text
			start_pos = match.start()
			end_pos = match.end()

			# Calculate the position in the new text without the anchor tags
			adjusted_start_pos = start_pos - offset
			adjusted_end_pos = adjusted_start_pos

			# Add phantom
			phantoms.append({"region": sublime.Region(adjusted_start_pos, adjusted_end_pos), "html": phantom_html})

			# Append the text before the match to the new text
			new_text += text[last_end:start_pos]
			last_end = end_pos

			# Update the offset to account for the removed anchor tags
			offset += len(match.group(0))

		self.view.erase_phantoms("pieces_phantom")
		# Append the remaining text after the last match
		new_text += text[last_end:]

		# Append the modified text to the view
		self.view.run_command('append', {'characters': new_text})

		# Add phantoms after append command
		for phantom in phantoms:
			self.view.add_phantom("pieces_phantom",phantom["region"], phantom["html"], sublime.LAYOUT_INLINE, on_navigate=self.on_nav)
	
	def on_nav(self,href):
		if href == "open_pieces":
			def run_async():
				version = open_pieces_os()
				if version:
					self.calls = {} # Clear the cache
					self.reload()
			sublime.set_timeout_async(run_async)


		elif href == "create_asset":
			new_file = self.view.window().new_file(syntax="Packages/Python/Python.sublime-syntax")
			new_file.run_command("append",{"characters":"print('I love Pieces')"})
			new_file.run_command("select_all")
			new_file.set_name("Create your first asset 🆕")
			new_file.set_scratch(True)
			new_file.show_popup("Right click to open your context menu Then go to 'Pieces > Save to Pieces'")
		elif href == "ask_question":
			new_file = self.view.window().new_file(syntax="Packages/Python/Python.sublime-syntax")
			new_file.run_command("append",{"characters":"I Love Pieces.upper()"})
			new_file.run_command("select_all")
			new_file.set_name("Ask for bug fix 🤔")
			new_file.set_scratch(True)
			new_file.show_popup("Right click to open your context menu Then go to 'Pieces > Ask Copilot > Fix Bug'")

		elif href == "open":
			self.view.window().run_command("pieces_list_assets")

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
		
		print(data)
		with open(cls.ONBOARDING_SETTINGS_PATH, "w") as f:
			json.dump(data, f, indent=4)

if not PiecesOnBoardingHandlerCommand.get_onboarding_settings().get("lunch_onboarding",False):
	sublime.active_window().run_command("pieces_onboarding")
	PiecesOnBoardingHandlerCommand.add_onboarding_settings(lunch_onboarding=True)