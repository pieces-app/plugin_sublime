import sublime_plugin
from ..settings import PiecesSettings


class PiecesOnboardingCommand(sublime_plugin.WindowCommand):
	def run(self):
		view = self.window.new_file(syntax=PiecesSettings.ONBOARDING_SYNTAX)
		
		text = """
[Success] Installed pieces
[Failed] Downloading dependencies
[In Progress] Run your first command
		""".strip()


		# Insert the text
		view.run_command('append', {'characters': text})
		# Set the name
		view.set_name("Welcome to Pieces!")
		# Set it to scratch to avoid the default saving menu
		view.set_scratch(True)
		# Set readonly
		view.set_read_only(True)
		# set the color scheme
		view.settings().set("color_scheme",PiecesSettings.ONBOARDING_COLOR_SCHEME)

		view.settings().set("line_numbers", False)