import datetime
from ..settings import PiecesSettings
import sublime_plugin
import sublime

class PiecesEnableLTMCommand(sublime_plugin.ApplicationCommand):
	def name(self):
		return "pieces_enable_ltm"

	def run(self):
		sublime.set_timeout_async(self.run_async)

	def run_async(self):
		try:
			PiecesSettings.api_client.copilot.context.ltm.enable(True) # True to show the permission message if it is missing
		except PermissionError:
			sublime.error_message("Failed to enable the LTM: Missing necessary permissions. Please check your user permissions and try again.")


class PiecesDisableLTMCommand(sublime_plugin.WindowCommand):
	def name(self):
		return "pieces_disable_ltm"

	def run(self,pause):
		self.pause = pause
		sublime.set_timeout_async(self.run_async)

	def run_async(self):
		until = datetime.datetime.now() + datetime.timedelta(minutes=self.pause) if self.pause else None
		PiecesSettings.api_client.copilot.context.ltm.pause(until)

	def input(self, args: dict):
		return PauseInputHandler()

class PauseInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		return [
			("Pause for 15 minutes",15),
			("Pause for 1 hour",60),
			("Pause for 6 hours",60*6),
			("Pause for 12 hours",60*12),
			("Pause for 24 hours",60*24),
			("Turn off",None)
		]

	def placeholder(self):
		return "How long will you pause the LTM for"

