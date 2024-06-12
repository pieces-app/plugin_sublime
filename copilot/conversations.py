from ..streamed_identifiers import StreamedIdentifiersCache
from ..settings import PiecesSettings
from pieces_os_client import ConversationApi

class ConversationsSnapshot(StreamedIdentifiersCache,
	api_call=ConversationApi(PiecesSettings.api_client).conversation_get_specific_conversation):
	
	@classmethod
	def sort_first_shot(cls):
		# Sort the dictionary by the "updated" timestamp
		sorted_conversations = sorted(cls.identifiers_snapshot.values(), key=lambda x: x.updated.value, reverse=True)
		cls.identifiers_snapshot = {conversation.id:conversation for conversation in sorted_conversations}