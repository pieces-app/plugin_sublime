import sublime
import sublime_plugin
from Pieces.settings import PiecesSettings


support_resources = [
	{
		"text":"Open a GitHub Issue",
		"value":"https://github.com/pieces-app/plugin_sublime/issues",
		"details":"Create an issue on our GitHub | https://github.com/pieces-app/plugin_sublime/issues"
	},
	{
		"text": "Feedback Form",
		"value": "https://getpieces.typeform.com/to/mCjBSIjF#page=sublime-plugin",
		"details": "We would love to hear your thoughts and suggestions about our Sublime Text plugin. | https://getpieces.typeform.com/to/mCjBSIjF#page=obsidian-plugin"
	},
	{
		"text":"Get Support",
		"value":"https://docs.pieces.app/support",
		"details":"Visit our website | https://docs.pieces.app/support"
	},
	{
		"text":"Join our Discord Server",
		"value":"https://discord.gg/getpieces",
		"details":"Chat with the Pieces team and our community of developers around the world | https://discord.gg/getpieces"
	}
]



class PiecesSupportCommand(sublime_plugin.ApplicationCommand):
	def run(self,support):
		PiecesSettings.open_website(support)
	def input(self,args):
		if not args.get("support",False):
			return SupportInputHandler()


class SupportInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		return [
			sublime.ListInputItem(**val) for val in support_resources
		]

	def placeholder(self):
		return "Want help?"