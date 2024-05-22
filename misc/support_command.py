import sublime
import sublime_plugin
import webbrowser


support_resources = [
	{
		"text":"Open a github issue",
		"value":"https://github.com/pieces-app/plugin_sublime/issues",
		"details":"Create a github issue on github | https://github.com/pieces-app/plugin_sublime/issues"
	},
	{
		"text":"Get support on our website",
		"value":"https://docs.pieces.app/support",
		"details":"Checkout our website | https://docs.pieces.app/support"
	},
	{
		"text":"Join our discord server",
		"value":"https://discord.gg/getpieces",
		"details":"Join our discord server | https://discord.gg/getpieces"
	}
]



class PiecesSupportCommand(sublime_plugin.ApplicationCommand):
	def run(self,support):
		webbrowser.open_new_tab(support)
	def input(self,args):
		return SupportInputHandler()


class SupportInputHandler(sublime_plugin.ListInputHandler):
	def list_items(self):
		return [
			sublime.ListInputItem(**val) for val in support_resources
		]

	def placeholder(self):
		return "Want help?"