"""
	Thanks to gitgutter package!
	https://github.com/jisaacks/GitGutter/tree/master/modules/popup
"""
import mdpopups
import sublime

class HtmlDiffer:
	"""
	A class to generate HTML output highlighting the differences between two sets of lines.
	"""

	def __init__(self,view, old_lines, new_lines):
		"""
		Initialize the HtmlDiffer with two sets of lines to compare.
		
		:param view: the view of the lines that you want to compare
		:param old_lines: List of lines representing the old version.
		:param new_lines: List of lines representing the new version.

		"""
		self.old_lines = old_lines
		self.new_lines = new_lines
		self.view = view

	def generate_diff(self,code_wrap):
		"""
		Generate the HTML string with highlighted differences.

		:return: A string containing the HTML representation of the differences.
		"""
		return ''.join(self._highlight_diff(code_wrap))

	def _highlight_diff(self,code_wrap):
		"""
		Internal generator function to yield HTML snippets with highlighted differences.

		:yield: HTML snippets as strings.
		"""
		div_map = self.diff_lines(self.old_lines, self.new_lines)
		yield '<div class="highlight"><pre>'

		text_chunk = ""
		old_tag = div_map[0][1]

		for line, tag in div_map:
			if tag != old_tag:
				yield self._highlight_chunk(tag,text_chunk,code_wrap)
				text_chunk = ""
				old_tag = tag
			text_chunk += line + "\n"

		if text_chunk:
			yield self._highlight_chunk(old_tag,text_chunk,code_wrap)
		
		yield '</pre></div>'


	def _highlight_chunk(self,_class,chunk,code_wrap):
		highlighted_line = mdpopups.syntax_highlight(self.view, chunk, language=mdpopups.get_language_from_view(self.view) or '', allow_code_wrap=code_wrap)
		highlighted_line = highlighted_line[28:-13] # Remove the pre,div begining classes
		return f'<span class="{_class}">{highlighted_line}</span>'


	def diff_lines(self, old_lines, new_lines):
		"""
		Create a diff map between two sets of lines using Myers' diff algorithm.

		:param old_lines: List of lines representing the old version.
		:param new_lines: List of lines representing the new version.
		:return: A list of tuples representing the diff map.
		"""
		trace = self.build_trace(old_lines, new_lines)
		return self.build_diff(trace, old_lines, new_lines)

	@staticmethod
	def build_trace(old_lines, new_lines):
		n, m = len(old_lines), len(new_lines)
		max_d = n + m
		v = [0] * (2 * max_d + 1)
		trace = []

		for d in range(max_d + 1):
			trace.append(v[:])
			for k in range(-d, d + 1, 2):
				if k == -d or (k != d and v[k - 1] < v[k + 1]):
					x = v[k + 1]
				else:
					x = v[k - 1] + 1
				y = x - k
				while x < n and y < m and old_lines[x] == new_lines[y]:
					x += 1
					y += 1
				v[k] = x
				if x >= n and y >= m:
					trace.append(v[:])
					return trace

	@staticmethod
	def build_diff(trace, old_lines, new_lines):
		n, m = len(old_lines), len(new_lines)
		x, y = n, m
		diff_map = []

		for d in range(len(trace) - 1, -1, -1):
			v = trace[d]
			k = x - y
			if k == -d or (k != d and v[k - 1] < v[k + 1]):
				prev_k = k + 1
			else:
				prev_k = k - 1
			prev_x = v[prev_k]
			prev_y = prev_x - prev_k
			while x > prev_x and y > prev_y:
				diff_map.append((old_lines[x - 1], "unchanged"))
				x -= 1
				y -= 1
			if x > prev_x:
				diff_map.append((old_lines[x - 1], "removed"))
				x -= 1
			elif y > prev_y:
				diff_map.append((new_lines[y - 1], "added"))
				y -= 1

		while x > 0:
			diff_map.append((old_lines[x - 1], "removed"))
			x -= 1
		while y > 0:
			diff_map.append((new_lines[y - 1], "added"))
			y -= 1

		diff_map.reverse()
		return diff_map


def show_diff_popup(view, old_lines, new_lines, on_nav,**kwargs):
	"""Show the diff popup.

	Arguments:
		view (sublime.View):
			The view object where the popup will be displayed.
		old_lines (list):
			The list of lines representing the old version.
		new_lines (list):
			The list of lines representing the new version.
		on_nav (callback):
			the callback that will be runned when the buttons is clicked
		kwargs (dict):
			Additional arguments for customization.
	"""
	point = kwargs.get('point', view.sel()[0].end() if view.sel() else None)
	if point is None:
		return

	line = view.rowcol(point)[0] + 1

	buttons = "<div class='toolbar'><a href=insert>✅ Accept</a> | <a href=dismiss style='color:red'>❌ Reject</a>"
	location = _visible_text_point(view, line - 1, 0)
	code_wrap = view.settings().get('word_wrap', 'auto') == 'auto' and view.match_selector(location, 'source')

	
	differ = HtmlDiffer(view,old_lines, new_lines).generate_diff(code_wrap=code_wrap)
	
	content = (
		buttons + 
		differ
	)

	popup_width = int(view.viewport_extent()[0])
	if code_wrap:
		line_length = view.settings().get('wrap_width', 0)
		if line_length > 0:
			popup_width = (line_length + 5) * view.em_width()

	popup_kwargs = {
		'view': view,
		'content': content,
		'md': False,
		'css': _load_popup_css(),
		"location": location,
		"max_width": popup_width,
		"flags":kwargs.get('flags', 0),
		"on_navigate":on_nav
	}
	
	view.hide_popup() # Remove any other popup in the view
	mdpopups.show_popup(**popup_kwargs,on_hide=lambda:mdpopups.show_popup(**popup_kwargs))



def _load_popup_css():
	"""Load and join popup stylesheets."""
	css_path = 'Packages/Pieces/ask/index.css'
	return sublime.load_resource(css_path)


def _visible_text_point(view, row, col):
	"""Return the text_point of row,col clipped to the visible viewport.

	Arguments:
		view (sublime.View): the view to return the text_point for
		row (int): the row to use for text_point calculation
		col (int): the column relative to the first visible column of the viewport which is defined by the horizontal scroll position.
	Returns:
		int: The text_point of row & col within the viewport.
	"""
	viewport = view.visible_region()
	_, vp_col = view.rowcol(viewport.begin())
	return view.text_point(row, vp_col + col)
