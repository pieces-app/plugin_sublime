from ..streamed_identifiers import StreamedIdentifiersCache
from ..settings import PiecesSettings
from pieces_os_client import AssetApi

class AssetSnapshot(StreamedIdentifiersCache,
	api_call=AssetApi(PiecesSettings.api_client).asset_snapshot):
	pass

def tabulate_from_markdown(md_text):
	# Split the markdown text into lines
	lines = md_text.split('\n')

	# Filter out lines that contain '|', and join them back into a string
	table_md = "\n".join(line for line in lines if '|' in line)

	# Split the markdown table into lines, and then into cells
	# Also, remove leading/trailing whitespace from each cell
	data = [[cell.strip() for cell in line.split("|")[1:-1]] for line in table_md.strip().split("\n")]

	headers = "<div>"
	for header in data[0]:
		if header:
			headers += "<span><h1>" + header + "</h1></span>"

    # Generate HTML string
	html_text = f"{headers}</div><br><div>"
	for row in data[2:]:
		html_text += "<div>"
		for idx,cell in enumerate(row):
			if idx == 0:
				cell += ": " 
			html_text += "<span>" + cell + "</span>"
		html_text += "<br><br></div>"
	html_text += "</div>"


	return md_text.replace(table_md,html_text)