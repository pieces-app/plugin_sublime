import sublime_plugin
import sublime
import textwrap
import re

from ...settings import PiecesSettings
from ...api import version_check
from ... import PiecesDependencies



class PiecesOnBoardingHandlerCommand(sublime_plugin.TextCommand):
	on_boarding_views = {} # Store the view id : some meta data
	def run(self,edit,mode="reload",point = None):
		self.edit = edit
		if mode == "reload":
			self.reload()
		elif mode == "hover":
			self.show_popup(point=point)

	def show_popup(point):
		popup_details = on_boarding_views[self.view.id()]
		for popup in popup_details:
			if point in popup["region"]:
				print(popup["url"])


	def reload(self):
		text = f"{self.pieces_os_status()}\n{self.dependencies_status()}"
		text = self.store_text_url(text)

		# Get the entire region of the view
		entire_region = sublime.Region(0, self.view.size())
		# set read only false
		self.view.set_read_only(False)
		# Erase the entire region
		self.view.erase(self.edit, entire_region)
		self.view.run_command('append', {'characters': text})
		# Set readonly
		self.view.set_read_only(True)

	@staticmethod
	def pieces_os_status():
		if PiecesSettings().get_health():
			check_version,update = version_check()
			if not check_version:
				return f"[Failed] You need to update {update}"
			return '[Success] Installed Pieces OS'
		return "[Failed] Please install Pieces OS"

	@staticmethod
	def dependencies_status():
		if PiecesDependencies.downloading:
			return "[In Progress] Downloading some dependencies"
		return "[Success] Downloaded some dependencies successfully"



	def store_text_url(self,text):
		# Regular expression to find command tags
		command_pattern = re.compile(r'<a href="(.*?)">(.*?)</a>')

		new_text = text
		offset = 0

		for match in command_pattern.finditer(text):
			# Get the span of the command text
			start, end = match.span(2)
			region = (start + offset, end + offset)

			# Replace the command text with something else
			replacement =  match.group(2)
			new_text = new_text[:region[0]] + replacement + new_text[region[1]:]

			# Calculate the new offset
			offset += len(replacement) - (end - start)

			# Update the region after replacement
			new_region = sublime.Region(region[0], region[0] + len(replacement))

			# Store the region and the command
			self.on_boarding_views[self.view.id()].append({"region":new_region,"url":match.group(1)})

		return new_text