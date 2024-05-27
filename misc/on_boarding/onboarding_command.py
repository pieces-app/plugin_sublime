import sublime_plugin

from ...settings import PiecesSettings
from .onboarding_handler import PiecesOnBoardingHandlerCommand
class PiecesOnboardingCommand(sublime_plugin.WindowCommand):
	
	def run(self):
		self.view = self.window.new_file(syntax = PiecesSettings.ONBOARDING_SYNTAX)
		# append the on_boarding_views
		PiecesOnBoardingHandlerCommand.on_boarding_views[self.view.id()] = []
		# Set the name
		self.view.set_name("Welcome to Pieces!")
		# Set it to scratch to avoid the default saving menu
		self.view.set_scratch(True)
		# set the color scheme
		self.view.settings().set("color_scheme",PiecesSettings.ONBOARDING_COLOR_SCHEME)
		# Remove lines numbers from the gutter
		self.view.settings().set("line_numbers", False)
		# reload the view
		self.view.run_command("pieces_on_boarding_handler")


