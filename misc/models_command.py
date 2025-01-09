import sublime_plugin
import sublime
from ..settings import PiecesSettings
from enum import Enum

class ModelsEnum(Enum):
	GPT_4o_MINI = ("GPT-4o Mini", "A more compact version of GPT-4o with a 128k-token context window, balancing capacity and efficiency.", "GPT-4o Mini Chat Model")
	GPT_4o = ("GPT-4o", "A high-output GPT-4 variant optimized for extended tasks, featuring a 128k-token context window.", "GPT-4o Chat Model")
	GPT_4_TURBO = ("GPT-4 Turbo", "A faster, cost-efficient version of GPT-4 with a 128k-token context window.", "GPT-4 Turbo Chat Model")
	GPT_4 = ("GPT-4", "An advanced model offering a robust 8k-token context window for high-quality responses.", "GPT-4 Chat Model")
	GPT_3_5_TURBO = ("GPT-3.5 Turbo", "A versatile language model with a 16k-token context window, ideal for general tasks.", "GPT-3.5-turbo Chat Model")
	PALM_2_CODE_CHAT_BISON = ("PaLM 2 Code Chat Bison", "A coding-optimized variant of PaLM 2 Chat Bison with a 4k-token context window.", "Codey (PaLM2) Chat Model")
	GEMINI_PRO_CHAT = ("Gemini Pro Chat", "A general-purpose language model with a standard context window size of 4k tokens.", "Gemini-1.5 Pro Chat Model")
	PALM_2_CHAT_BISON = ("PaLM 2 Chat Bison", "Google's conversational AI tuned for dialogue, offering a 4k-token context window.", "(PaLM2) Chat Model")
	GEMINI_1_5_PRO = ("Gemini 1.5 Pro", "An advanced version of Gemini, featuring an expanded context window of 128k tokens for enhanced context retention.", "Gemini-1.5 Pro Chat Model")
	GEMINI_1_5_FLASH = ("Gemini 1.5 Flash", "A lightweight version of Gemini 1.5 Pro, optimized for speed, with up to a 256k-token context window.", "Gemini-1.5 Flash Chat Model")
	CLAUDE_3_5_SONNET = ("Claude 3.5 Sonnet", "An upgrade to Claude 3 Sonnet, retaining the 40k-token context window but with improved reasoning.", "Claude 3.5 Sonnet Chat Model")
	CLAUDE_3_SONNET = ("Claude 3 Sonnet", "A creative AI designed for eloquent writing, offering a 40k-token context window for in-depth compositions.", "Claude 3 Sonnet Chat Model")
	CLAUDE_3_OPUS = ("Claude 3 Opus", "A high-capacity model designed for detailed analysis and creation, supporting a 40k-token context window.", "Claude 3 Opus Chat Model")
	CLAUDE_3_HAIKU = ("Claude 3 Haiku", "A concise, creative LLM with a 40k-token context window for shorter tasks requiring precision.", "Claude 3 Haiku Chat Model")
	PHI_3_MINI_4K = ("Phi-3 Mini 4K", "A miniaturized version of Phi-3 with a 4k-token context window, designed for efficient small-scale tasks.", "Phi-3-mini-4k-instruct")
	PHI_3_MINI_128K = ("Phi-3 Mini 128K", "A scaled-up version of Phi-3 Mini, supporting a 128k-token context window for extended context needs.", "Phi-3-mini-128k-instruct")
	PHI_2 = ("Phi-2", "A compact and efficient model with a 4k-token context window, suitable for lightweight applications.", "Phi-2 Chat Model")
	LLAMA_3_8B = ("LLaMA 3 8B", "The next generation of LLaMA, with 8 billion parameters and an enhanced 8k-token context window.", "Llama-3 8B Instruct")
	LLAMA_2_7B = ("LLaMA 2 7B", "A lightweight model with 7 billion parameters and a 4k-token context window, suitable for general use.", "Llama-2 7B Chat Model")
	GEMMA_1_1_7B = ("Gemma 1.1 7B", "A larger version of Gemma with 7 billion parameters and a 4k-token context window, offering greater capacity.", "gemma-1.1-7b-it")
	GEMMA_1_1_2B = ("Gemma 1.1 2B", "A streamlined LLM with 2 billion parameters and a 4k-token context window, designed for efficient performance.", "gemma-1.1-2b-it")
	CODE_GEMMA_1_1_7B = ("Code Gemma 1.1 7B", "A coding-specialized version of Gemma 1.1 with 7 billion parameters and a 4k-token context window.", "codegemma-1.1-7b-it")
	GRANITE_8B = ("Granite 8B", "A more robust version of Granite, featuring 8 billion parameters and a 4k-token context window for more complex tasks.", "granite-8b-code-instruct")
	GRANITE_3B = ("Granite 3B", "A versatile model with 3 billion parameters and a 4k-token context window, suitable for lightweight applications.", "granite-3b-code-instruct")
	

	def __init__(self, readable_name, description, unique_id):
		self._readable_name = readable_name
		self._description = description
		self._unique_id = unique_id

	@property
	def name(self):
		return self._readable_name

	@property
	def description(self):
		return self._description

	@property
	def unique_id(self):
		return self._unique_id

	@classmethod
	def get(cls, unique_id):
		for model in cls:
			if model.unique_id == unique_id:
				return model
		return None



class PiecesChangeModelCommand(sublime_plugin.ApplicationCommand):
	def run(self, model_id):
		settings = PiecesSettings.get_settings()
		settings["model"] = model_id
		sublime.save_settings("Pieces.sublime-settings")
		PiecesSettings.on_settings_change()

	def input(self,args):
		return ModelsInputHandler()



class ModelsInputHandler(sublime_plugin.ListInputHandler):
	def name(self) -> str:
		return "model_id"

	def placeholder(self) -> str:
		model = ModelsEnum.get(PiecesSettings.api_client.model_name)
		if model:
			return f"Currently using {model.name}"
		return "Select a Model"

	def list_items(self):
		return [sublime.ListInputItem(
				text=model.name,
				value=model.unique_id,
				details=model.description) for model in ModelsEnum]

