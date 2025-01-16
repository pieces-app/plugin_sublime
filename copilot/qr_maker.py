from typing import List, Tuple
import sublime
import sublime_plugin
from .ask_command import copilot
import json
import time
from ..settings import PiecesSettings

lock = False

class PiecesShowQRCodesCommand(sublime_plugin.TextCommand):
	def name(self):
		return "pieces_show_qr_codes"
	def run(self, edit: sublime.Edit, force = False):
		self.api_copilot = PiecesSettings.api_client.copilot
		self.ltm = self.api_copilot.context.ltm

		global lock
		if (lock or not self.ltm.is_chat_ltm_enabled):
			if not force: return

		lock = True # lock no more operations until the QRCode is removed
		self.removes:List[List[int]] = []  # Regions to remove after the QR is captured
		self.edit = edit
		self.show_qr()

	def get_qr(self) -> str:
		return f"<img src='{self.ltm.get_qrcode()}' />"

	def show_qr(self):
		window = self.view.window()
		if window: window.run_command("hide_panel")

		copilot.can_type = False  # Prevent typing
		copilot.cache_response = True # cache the response don't add anything to the view
		self.view.settings().set("word_wrap", False) # Wrap text to avoid miss calculate
		lines = self.view.lines(sublime.Region(0, self.view.size()))
		lines_count = len(lines)
		min_lines, min_width = self._max_char()

		if lines_count < min_lines:  # Create new lines if needed
			size = self.view.size()
			lines_to_insert = int(min_lines - lines_count)
			self.removes.append([size, size + lines_to_insert])
			self.view.insert(self.edit, size, "\n" * lines_to_insert)
			lines = self.view.lines(sublime.Region(0, self.view.size())) # Update the lines after we added the new ones



		target_line = lines[int(min_lines) - 1 - int(self._qr_height_lines())]
		point = target_line.begin() - 1
		self.view.insert(self.edit,point,"\n") # add inset just before the line that we want add to
		self.removes.append([point,point+1])
		line = self.view.line(point + 1)
		width = (line.end() - line.begin())
		chars_to_insert = int(min_width - line.size())
		if width < min_width:
			self.removes.append([line.end(), line.end() + chars_to_insert])
			self.view.insert(self.edit, line.end(), " " * chars_to_insert)

		bottom_right_position = (line.end() + chars_to_insert) - int(self._qr_width_characters())

		self.view.add_phantom("qr_top", sublime.Region(0, 0), self.get_qr(), layout=sublime.PhantomLayout.INLINE)
		self.view.add_phantom("qr_bottom", sublime.Region(bottom_right_position, bottom_right_position), self.get_qr(), layout=sublime.PhantomLayout.INLINE)

		sublime.set_timeout_async(self.loop_viewport)
		sublime.set_timeout(self.remove_qr, 4000)  # Wait max 4 sec to remove the QR Code
		sublime.set_timeout_async(self.capture, 4000) # Capture the codes wait for 4 sec 


	def capture(self):
		# @mack-at-pieces do I need to do any checks here to make sure it selected to correct window?
		self.ltm.capture()
		self.remove_qr()

	def loop_viewport(self):
		# Avoid user from scrolling until we capture the QRCodes
		self.view.set_viewport_position((0,0), False)
		time.sleep(0.2)
		if lock:
			self.loop_viewport()

	def remove_qr(self):
		self.removes.reverse() # remove every thing I did add to be able to remove it the correct order
		self.view.run_command("pieces_remove_qr_codes", args={"removes": json.dumps(self.removes)})

	def _max_char(self) -> Tuple[float, float]:
		viewport_width, viewport_height = self.view.viewport_extent()
		line_height = self.view.line_height()
		return viewport_height // line_height, viewport_width // self.view.em_width()

	def _qr_height(self) -> int:
		"""
			returns the height of the QR code the width = height
		"""
		return 50 # This should not change except if you change the QRCode image it self

	def _qr_height_lines(self):
		"""
			Returns the number of lines that the qr code will take
		"""
		return (self._qr_height() // self.view.line_height()) + 2 # some offset

	def _qr_width_characters(self):
		"""
			Returns the number of characters that the qr code will take
		"""
		return (self._qr_height() // self.view.em_width()) + 4 # some offset


	def is_enabled(self) -> bool:
		return bool(self.view.settings().get("PIECES_GPT_VIEW",False))

class PiecesRemoveQrCodes(sublime_plugin.TextCommand):
	def run(self, edit: sublime.Edit, removes):
		global lock
		if not lock:
			return
		self.view.settings().set("word_wrap", True) # Return it to false again NOT AUTO because the copilot is False by default
		lock = False
		removes = json.loads(removes)
		copilot.can_type = True
		copilot.cache_response = False
		self.view.erase_phantoms("qr_top")
		self.view.erase_phantoms("qr_bottom")

		for remove in removes:
			self.view.erase(edit, sublime.Region(*remove))

