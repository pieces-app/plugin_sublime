import sublime
import sublime_plugin
import asyncio
import threading
import mdpopups
import urllib.request
import base64

from pieces import main
from pieces import config
from .copilot_css_classes import *



class PiecesAskStreamCommand(sublime_plugin.WindowCommand):
    sheet_id = None
    header = f"<h1> Pieces Copilot </h1>" # TODO Add conversation name
    footer = f"""<a href='subl:{sublime.html_format_command("pieces_ask_stream")}'>Ask a follow up question</a>""" # TODO Add footer 
    content_html = ''
    
    def run(self):
        # Check if the file already exists
        files = [sheet for sheet in self.window.sheets() if sheet.id() == PiecesAskStreamCommand.sheet_id]

        self.user_image = self.get_image_as_base64(main.USER_IMAGE_URL)
        self.conversation = None
        PiecesAskStreamCommand.dummy_view = self.window.create_output_panel('mdpopups-dummy', unlisted=True)
        self.author = None

        if files:
            # If the file exists, use the first one
            self.output_sheet = files[0]
            self.window.focus_sheet(self.output_sheet)
        else:
            # If the sheet doesn't exist, create a new one
            
            self.output_sheet = mdpopups.new_html_sheet(self.window,"Pieces Copilot",self.return_page(footer=False)+PIECES_IMAGE_TAG,md=False ,flags =sublime.NewFileFlags.NONE )
            PiecesAskStreamCommand.sheet_id = self.output_sheet.id()
        
        # Create a new tab
        self.window.show_input_panel("Ask Copilot:", "", self.on_done, None, None)


    @classmethod
    def return_page(cls,content = None,footer=True):
        """
        The main page of the stream view sheet which have the header footer and some content between   
        """
        code_css="code {display: block; width:100px; }" # This is the class for the code rendering
        css = f"<style>{code_css}</style>"
        
        html = cls.content_html + content if content else cls.content_html
        footer_html = cls.footer if footer else ''

        message_wraper = f'<div style="{MESSAGE_WRAPER_CLASS}">{html}</div>'
        return  f"<body id='pieces-ask-stream'>{css}{cls.header}{message_wraper}{footer_html}</body>"

    @staticmethod
    def get_image_as_base64(url):
        with urllib.request.urlopen(url) as response:
            image_content = response.read()
        base64_image = base64.b64encode(image_content)

        return f"data:image/jpeg;base64,{base64_image.decode('utf-8')}"

    def on_done(self, user_input):
        self.append_md(user_input,"user")

        # Start the message generator
        self.message_generator = main.ws_manager.message_generator(config.model_id, user_input)

        # Create a new thread and start an asyncio event loop in that thread
        def start_loop(loop):
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.display_message())

        new_loop = asyncio.new_event_loop()
        threading.Thread(target=start_loop, args=(new_loop,)).start()

    def append_md(self,message,author=None):
        if author:
            if author == "user":
                PiecesAskStreamCommand.content_html += self.user_html(message)
            elif author == "copilot":
                PiecesAskStreamCommand.content_html += self.copilot_html(message)
        else:
            PiecesAskStreamCommand.content_html += message
        mdpopups.update_html_sheet(self.output_sheet,self.return_page())


    def user_html(self,message):
        html = mdpopups.md2html(PiecesAskStreamCommand.dummy_view,message) 
        return f"<div style='text-align:right;margin-bottom:25px;'><div style='{USER_CLASS}'>{html}</div><div style='display:inline;border-radius: 20px'><img style='{IMAGE_CLASS}' src='{self.user_image}' /></div></div>"



    def copilot_html(self,message):
        html = mdpopups.md2html(PiecesAskStreamCommand.dummy_view,message)
        return f"<div style='margin-bottom:25px;'><div style='{COPILOT_CLASS}'> {html} </div></div>"

    async def display_message(self):
        self.stream_message = ""
        # Loop over the message generator
        async for message in self.message_generator:
            # message = message.replace("<","&lt;") # replace the <
            # message = message.replace(">","&gt;") # replace the >

            # This function will be run on a separate thread

            self.stream_message += message
            mdpopups.update_html_sheet(self.output_sheet,self.return_page(self.copilot_html(self.stream_message),False))
            # Run the append function asynchronously
            # sublime.set_timeout_async(append, 0)
        self.append_md(main.ws_manager.final_answer,"copilot")

