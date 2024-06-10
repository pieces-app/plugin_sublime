from pieces_os_client import QGPTQuestionInput, QGPTStreamInput, QGPTStreamOutput, RelevantQGPTSeed, RelevantQGPTSeeds
from ..settings import PiecesSettings
from sublime import Region
import sublime_plugin
from .ask_websocket import AskStreamWS


class PiecesAskStreamCommand(sublime_plugin.WindowCommand):
	gpt_view = None

	def run(self):
		if self.gpt_view:
			try:
				self.window.focus_view(self.gpt_view)
				return
			except Exception as e:
				print(e)
				self.gpt_view = None 
		PiecesAskStreamCommand.gpt_view = self.window.new_file(syntax="Packages/Markdown/Markdown.sublime-syntax")	
		
		self.gpt_view.settings().set("PIECES_GPT_VIEW",True) # Label the view as gpt view
		self.gpt_view.set_scratch(True)
		self.show_cursor()

	def show_cursor(self):
		self.gpt_view.run_command("append",{"characters":">>> "})

	def on_message_callback(self,message: QGPTStreamOutput):
		if message.question:
			answers = message.question.answers.iterable

			for answer in answers:
				text = answer.text
				self.gpt_view.run_command("append",{"characters":text})
		if message.status == "COMPLETED":
			PiecesEnterResponse.end_response = self.gpt_view.size() # Update the size
			self.gpt_view.set_read_only(False)
			self.show_cursor()
			
class PiecesEnterResponse(sublime_plugin.TextCommand):
	conversation_id = None
	end_response = 0 # Store the region of the response 

	def run(self,edit):
		PiecesAskStreamCommand.gpt_view.set_read_only(True)
		AskStreamWS().send_message(
			QGPTStreamInput(
				question=QGPTQuestionInput(
					query = self.view.substr(Region(self.end_response,self.view.size())),
					relevant = RelevantQGPTSeeds(iterable=[]),
					application=PiecesSettings.get_application().id,
					model = PiecesSettings.model_id
				),
				conversation = self.conversation_id,
				
			)
		)