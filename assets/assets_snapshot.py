from typing import Optional
import sublime


from ..streamed_identifiers import StreamedIdentifiersCache
from .._pieces_lib.pieces_os_client import (Asset, 
											AssetApi,
											ClassificationSpecificEnum,
											FormatApi,
											ClassificationGenericEnum)
from ..settings import PiecesSettings

class AssetSnapshot(StreamedIdentifiersCache,
	api_call=AssetApi(PiecesSettings.api_client).asset_snapshot):
	def __init__(self,asset_id) -> None:
		self._asset_id = asset_id
		self.asset = self.get_asset(asset_id)
		super().__init__()
	
	@classmethod
	def get_asset(cls,asset_id) -> Optional[Asset]:
		return cls.identifiers_snapshot.get(asset_id)

	def original_classification_specific(self) -> Optional[ClassificationSpecificEnum]:
		if self.asset:
			return self.asset.original.reference.classification.specific

	def edit_asset_original_format(self,data) -> None:
		if not self.asset:
			raise AttributeError("Asset not found")
		format_api = FormatApi(PiecesSettings.api_client)
		original = format_api.format_snapshot(self.asset.original.id, transferable=True)
		if original.classification.generic == ClassificationGenericEnum.IMAGE:
			# TODO: Ability to edit images
			sublime.error_message("Could not edit an image")
			return

		if original.fragment.string.raw:
			original.fragment.string.raw = data
		elif original.file.string.raw:
			original.file.string.raw = data
		format_api.format_update_value(transferable=False, format=original)

	def get_asset_raw(self) -> Optional[str]:
		if not self.asset:
			return
		asset_reference = self.asset.original.reference
		if asset_reference.fragment:
			return asset_reference.fragment.string.raw
		elif asset_reference.file.string:
			return asset_reference.file.string.raw
	@property
	def name(self) -> Optional[str]:
		return self.asset.name if self.asset else None
	
	@staticmethod
	def sort_first_shot():
		pass