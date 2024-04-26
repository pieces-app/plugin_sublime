import sublime
import sublime_plugin
from pieces.api import get_health



class PiecesEventListener(sublime_plugin.EventListener):
    def on_window_command(self, view, command_name, args):
        
        # List of commands to check
        commands_to_check = ['pieces_list_assets']
        self.check(command_name,commands_to_check)
        
    def on_text_command(self,view,command_name,args):
        commands_to_check = ['pieces_create_asset',"pieces_ask_question"]
        self.check(command_name,commands_to_check)

    def check(self,command_name,commands_to_check):
        if command_name in commands_to_check:
            if not get_health():
                sublime.message_dialog("The pieces os server is not running")
                return False
        return None
        


