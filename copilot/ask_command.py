from pieces_os_client import QGPTQuestionOutput
import sublime_plugin



class AskStreamCommand(sublime_plugin.WindowCommand):
	

	def on_message_callback(self,message: QGPTQuestionOutput):
		print(message)
