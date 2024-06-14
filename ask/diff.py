"""
	Thanks to gitgutter package!
	https://github.com/jisaacks/GitGutter/tree/master/modules/popup
"""
import mdpopups
from mdpopups.pygments import highlight
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
		highlighted_line = highlighted_line[28:-13]
		return f'<span class="{_class}">{highlighted_line}</span>'


	def diff_lines(self, old_lines, new_lines):
		"""
		Create a diff map between two sets of lines.

		:param old_lines: List of lines representing the old version.
		:param new_lines: List of lines representing the new version.
		:return: A list of tuples representing the diff map.
		"""
		# Create a 2D array to store the lengths of longest common subsequence
		lcs = [[0] * (len(new_lines) + 1) for _ in range(len(old_lines) + 1)]

		# Fill the lcs array
		for i in range(1, len(old_lines) + 1):
			for j in range(1, len(new_lines) + 1):
				if old_lines[i - 1] == new_lines[j - 1]:
					lcs[i][j] = lcs[i - 1][j - 1] + 1
				else:
					lcs[i][j] = max(lcs[i - 1][j], lcs[i][j - 1])

		# Backtrack to find the diff
		i, j = len(old_lines), len(new_lines)
		div_map = []

		while i > 0 and j > 0:
			if old_lines[i - 1] == new_lines[j - 1]:
				div_map.append((old_lines[i - 1], "unchanged"))
				i -= 1
				j -= 1
			elif lcs[i - 1][j] >= lcs[i][j - 1]:
				div_map.append((old_lines[i - 1], "removed"))
				i -= 1
			else:
				div_map.append((new_lines[j - 1], "added"))
				j -= 1

		# Add remaining lines
		while i > 0:
			div_map.append((old_lines[i - 1], "removed"))
			i -= 1
		while j > 0:
			div_map.append((new_lines[j - 1], "added"))
			j -= 1

		# Reverse to get the correct order
		div_map.reverse()
		return div_map




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

	popup_kwargs = {
		'view': view,
		'content': content,
		'md': False,
		'css': _load_popup_css()
	}

	popup_width = int(view.viewport_extent()[0])
	if code_wrap:
		line_length = view.settings().get('wrap_width', 0)
		if line_length > 0:
			popup_width = (line_length + 5) * view.em_width()
	mdpopups.show_popup(location=location, max_width=popup_width, flags=kwargs.get('flags', 0), on_navigate=on_nav, **popup_kwargs)




def _load_popup_css():
	"""Load and join popup stylesheets."""
	css_lines = []
	for path in ('Packages/Pieces', 'Packages/User'):
		try:
			css_path = path + '/ask/index.css'
			css_lines.append(sublime.load_resource(css_path))
		except IOError:
			pass
	return ''.join(css_lines)


def _get_min_indent(lines, tab_width=4):
	"""Find the minimum count of indenting whitespaces in lines.

	Arguments:
		lines (tuple): The content to search the minimum indention for.
		tab_width (int): The number of spaces expand tabs before searching for indention by.
	"""
	min_indent = 2**32
	for line in lines:
		i = 0
		for c in line:
			if c == ' ':
				i += 1
			elif c == '\t':
				i += tab_width - (i % tab_width)
			else:
				break
		if min_indent > i:
			min_indent = i
		if not min_indent:
			break
	return min_indent


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
