import sublime
import sublime_plugin
from pieces.api import get_health



class PiecesEventListener(sublime_plugin.EventListener):
    def on_window_command(self, view, command_name, args):
        # List of commands to check
        commands_to_check = ['pieces_list_assets','pieces_handle_markdown']
        if command_name in commands_to_check and not self.check_condition():
            sublime.message_dialog("The pieces os server is not running")
            # Cancel the command by replacing it with a no-op
            return None
        
    def check_condition(self):
        if get_health():
            return True
        return False



