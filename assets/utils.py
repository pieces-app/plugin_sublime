from ..streamed_identifiers import StreamedIdentifiersCache
import re

from .._pieces_lib.pieces_os_client import Asset, AssetApi,StreamedIdentifiers
import sublime

from ..settings import PiecesSettings

class AssetSnapshot(StreamedIdentifiersCache,
	api_call=AssetApi(PiecesSettings.api_client).asset_snapshot):
	pass

def tabulate_from_markdown(md_text):
	table_regex = re.compile(r'(\|.*\|(?:\n\|.*\|)+)')
	match = table_regex.search(md_text)

	if match:
		table_md = match.group(1)
	else: return md_text



	# Split the markdown table into lines, and then into cells
	# Also, remove leading/trailing whitespace from each cell
	data = [[cell.strip() for cell in line.split("|")[1:-1]] for line in table_md.strip().split("\n")]

    # Generate HTML string
	html_text = f"<h3>{data[0][0]}</h3><br><div>"
	for row in data[2:]:
		html_text += "<div>"
		for idx,cell in enumerate(row):
			if idx == 0:
				cell += ": " 
			html_text += "<span>" + cell + "</span>"
		html_text += "<br><br></div>"
	html_text += "</div>"


	return md_text.replace(table_md,html_text)
