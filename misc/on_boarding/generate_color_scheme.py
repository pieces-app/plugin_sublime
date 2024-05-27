import json
import os
import sublime
import ast

from ...settings import PiecesSettings


class ColorSchemeGenerator:
	resolved_value = None

	@staticmethod
	def load_resource(resource_str, color_scheme):
		try:
			# Attempt to load the resource as JSON
			resource = json.loads(resource_str)
			globals_ = resource["globals"]
			variables = resource["variables"]
		except json.decoder.JSONDecodeError:
			try:
				# If JSON loading fails, attempt to evaluate the resource string as a Python literal
				resource = ast.literal_eval(resource_str)
				globals_ = resource["globals"]
				variables = resource["variables"]
			except (ValueError, SyntaxError):
				# If both methods fail, fall back to default values
				globals_ = {
					"background": "var(background)",
					"foreground": "var(foreground)"
				}
				variables = {
					"background": color_scheme["palette"]["background"],
					"foreground": color_scheme["palette"]["foreground"]
				}
		
		return globals_, variables


	@staticmethod
	def get_color_scheme(globals_,variables):
		return  {
			"name": "Pieces color scheme",
			"globals": globals_,
			"variables": variables,
			"rules": [
				{
					"scope": "pieces.onboarding.success",
					"foreground": "#99c794"
				},
				{
					"scope": "pieces.onboarding.fail",
					"foreground": "#ec5f66"
				},
				{
					"scope":"pieces.onboarding.progress",
					"foreground": "#808080"
				},
			]
		}

	@classmethod
	def generate_color_scheme(cls):
		color_scheme = sublime.ui_info()["color_scheme"]
		resolved_value = color_scheme["resolved_value"]

		if resolved_value == cls.resolved_value:
			return # No change in the color scheme

		# Theme changed!
		cls.resolved_value = resolved_value
		resource_str = sublime.load_resource(sublime.find_resources(resolved_value)[0])

		globals_,variables = cls.load_resource(resource_str,color_scheme)

		path = os.path.join(
			sublime.packages_path(),
			PiecesSettings.ONBOARDING_COLOR_SCHEME
		)

		directory = os.path.dirname(path)
		
		if not os.path.exists(directory):
			os.makedirs(directory)
		

		with open(path, 'w') as f: 
			json.dump(cls.get_color_scheme(globals_,variables), f,indent=4)

