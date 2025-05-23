import sublime_plugin
import sublime
from enum import Enum
from .models_download_ws import ModelDownloadWS
from ...progress_bar import ProgressBar
from ...settings import PiecesSettings
from ...startup_utils import check_pieces_os
from ..._pieces_lib.pieces_os_client.models import ModelDownloadProgress, ModelDownloadProgressStatusEnum
from ..._pieces_lib.pieces_os_client.wrapper.websockets import BaseWebsocket

class ModelStatus(Enum):
	cloud = "Cloud"
	downloaded = "Downloaded"
	downloading = "Downloading"
	download = "Download"

class ModelsEnum(Enum):
	GEMINI_PRO = ("gemini-pro", "Gemini Pro Chat", "A general-purpose language model with a standard context window size of 4k tokens.")
	GEMINI_1_5_FLASH = ("gemini-1.5-flash", "Gemini 1.5 Flash", "A lightweight version of Gemini 1.5 Pro, optimized for speed, with up to a 256k-token context window.")
	GEMINI_1_5_PRO = ("gemini-1.5-pro", "Gemini 1.5 Pro", "An advanced version of Gemini, featuring an expanded context window of 128k tokens for enhanced context retention.")
	GEMINI_2_FLASH_EXP = ("gemini-2.0-flash-exp", "Gemini 2.0 Flash Experimental", "An advanced iteration in Google's Gemini series optimized for rapid response times and efficient processing. Includes architectural improvements from Gemini 1.5 while maintaining competitive language understanding.")
	GEMINI_2_FLASH_LITE = ("gemini-2.0-flash-lite-001", "Gemini 2.0 Flash Lite", "Gemini 2.0 Flash Lite offers a significantly faster time to first token (TTFT) compared to Gemini Flash 1.5, while maintaining quality on par with larger models like Gemini Pro 1.5, all at extremely economical token prices.")
	GEMINI_2_5_PRO_EXP = ("gemini-2.5-pro-exp-03-25", "Gemini 2.5 Pro Experimental", "Gemini 2.5 Pro is Google’s state-of-the-art AI model designed for advanced reasoning, coding, mathematics, and scientific tasks.")
	GEMINI_2_5_FLASH_PREVIEW = ("gemini-2.5-flash-preview-04-17", "Gemini 2.5 Flash Preview 04-17", "Gemini 2.5 Flash is Google's state-of-the-art workhorse model, specifically designed for advanced reasoning, coding, mathematics, and scientific tasks.")
	GEMINI_2_5_PRO_PREVIEW = ("gemini-2.5-pro-preview-03-25", "Gemini 2.5 Pro Preview", "Gemini 2.5 Pro is Google’s state-of-the-art AI model designed for advanced reasoning, coding, mathematics, and scientific tasks.")
	CLAUDE_3_SONNET = ("claude-3-sonnet-20240229", "Claude 3 Sonnet", "A creative AI designed for eloquent writing, offering a 40k-token context window for in-depth compositions.")
	CLAUDE_3_HAIKU = ("claude-3-haiku-20240307", "Claude 3 Haiku", "A concise, creative LLM with a 40k-token context window for shorter tasks requiring precision.")
	CLAUDE_3_OPUS = ("claude-3-opus-20240229", "Claude 3 Opus", "A high-capacity model designed for detailed analysis and creation, supporting a 40k-token context window.")
	CLAUDE_3_5_SONNET = ("claude-3-5-sonnet-20241022", "Claude 3.5 Sonnet", "An upgrade to Claude 3 Sonnet, retaining the 40k-token context window but with improved reasoning.")
	CLAUDE_3_5_HAIKU = ("claude-3-5-haiku-20241022", "Claude 3.5 Haiku", "Claude 3.5 Haiku features enhancements across all skill sets including coding, tool use, and reasoning. As the fastest model in the Anthropic lineup, it offers rapid response times suitable for applications that require high interactivity and low latency, such as user-facing chatbots and on-the-fly code completions.")
	CLAUDE_3_7_SONNET = ("claude-3-7-sonnet-20250219", "Claude 3.7 Sonnet", "Claude 3.7 Sonnet is an advanced large language model with improved reasoning, coding, and problem-solving capabilities. It introduces a hybrid reasoning approach, allowing users to choose between rapid responses and extended, step-by-step processing for complex tasks. The model demonstrates notable improvements in coding, particularly in front-end development and full-stack updates, and excels in agentic workflows, where it can autonomously navigate multi-step processes.")
	GPTO_4_MINI = ("o4-mini-2025-04-16", "OpenAI o4 Mini", "OpenAI o4-mini is a compact reasoning model in the o-series, optimized for fast, cost-efficient performance while retaining strong multimodal and agentic capabilities. It supports tool use and demonstrates competitive reasoning and coding performance across benchmarks like AIME (99.5% with Python) and SWE-bench, outperforming its predecessor o3-mini and even approaching o3 in some domains.")
	GPTO_3_MINI = ("o3-mini-2025-01-31", "OpenAI o3 Mini", "OpenAI o3-mini is a cost-efficient language model optimized for STEM reasoning tasks, particularly excelling in science, mathematics, and coding.")
	GPTO_3 = ("o3-2025-04-16", "OpenAI GPT-o3", "o3 is a well-rounded and powerful model across domains. It sets a new standard for math, science, coding, and visual reasoning tasks. It also excels at technical writing and instruction-following.")
	GPTO_1 = ("o1-2024-12-17", "OpenAI GPT-o1", "Designed to spend more time thinking before responding. The o1 model series is trained with large-scale reinforcement learning to reason using chain of thought.")
	GPT4_1 = ("gpt-4.1-2025-04-14", "OpenAI GPT-4.1", "GPT-4.1 is a flagship large language model optimized for advanced instruction following, real-world software engineering, and long-context reasoning. It supports a 1 million token context window and outperforms GPT-4o and GPT-4.5.")
	GPT4O_MINI = ("gpt-4o-mini", "OpenAI GPT-4o Mini", "A more compact version of GPT-4o with a 128k-token context window, balancing capacity and efficiency.")
	GPT4O = ("gpt-4o", "OpenAI GPT-4o", "A high-output GPT-4 variant optimized for extended tasks, featuring a 128k-token context window.")
	GPT4_TURBO = ("gpt-4-turbo", "OpenAI GPT-4 Turbo", "A faster, cost-efficient version of GPT-4 with a 128k-token context window.")
	GPT4 = ("gpt-4", "OpenAI GPT-4", "An advanced model offering a robust 8k-token context window for high-quality responses.")
	GPT3_5 = ("gpt-3.5-turbo", "OpenAI GPT-3.5", "A versatile language model with a 4k-token context window, suitable for general tasks.")
	CODECHAT_BISON = ("codechat-bison", "Google PaLM 2 Code Chat 32k", "PaLM 2 fine-tuned for chatbot conversations that help with code-related questions.")
	CHAT_BISON = ("chat-bison", "Google PaLM 2 Code Chat 32k", "PaLM 2 is a language model by Google with improved multilingual, reasoning and coding capabilities.")
	PHI2 = ("phi:2.7b-chat-v2-q4_K_S", "Phi-2", "A compact and efficient model with a 4k-token context window, suitable for lightweight applications.")
	PHI3MINI_4K = ("phi3:3.8b-mini-4k-instruct-q4_K_S", "Phi-3 Mini 4K", "A miniaturized version of Phi-3 with a 4k-token context window, designed for efficient small-scale tasks.")
	PHI3MINI_128K = ("phi3:3.8b-mini-128k-instruct-q4_K_S", "Phi-3 Mini 128K", "A scaled-up version of Phi-3 Mini, supporting a 128k-token context window for extended context needs.")
	PHI3MEDIUM_14B_4K = ("phi3:14b-medium-4k-instruct-q4_K_S", "Phi-3 Medium 14B 4K", "A 14B parameter language model from Microsoft's Phi model series, designed for medium-scale tasks with a 4K context window. Part of Microsoft's research into efficient and scalable language models.")
	PHI3MEDIUM_14B_128K = ("phi3:14b-medium-128k-instruct-q4_K_S", "Phi-3 Medium 14B 128K", "Extended context version of the Phi-3 14B model, featuring a 128K token context window. Optimized for longer-form content while maintaining the base model's capabilities.")
	PHI3_5MINI_3_8B = ("phi3.5:3.8b-mini-instruct-q4_K_S", "Phi-3.5 Mini 3.8B", "A compact 3.8B parameter model from Microsoft's Phi series, designed for efficient deployment while maintaining strong performance on general language tasks.")
	PHI4_14B = ("phi4:14b-q4_K_M", "Phi-4 14B", "A 14B parameter language model in Microsoft's Phi series, representing a significant advancement in model capabilities while maintaining the series' focus on efficiency and reliable performance.")
	MISTRAL_7B = ("mistral:7b-instruct-q4_K_S", "Mistral 7B", "A compact model with 7 billion parameters and a 4k-token context window, optimized for efficient processing.")
	MIXTRAL8_7B = ("mixtral:8x7b-instruct-v0.1-q4_K_S", "Mixtral 8 7B", "An open-source mixture-of-experts model from Mistral AI, combining strong performance with efficient computation through selective expert activation.")
	LLAMA2_7B = ("llama2:7b-chat-q4_K_S", "Llama 2 7B", "A lightweight model with 7 billion parameters and a 4k-token context window, suitable for general use.")
	LLAMA2_13B = ("llama2:13b-chat-q4_K_S", "Llama 2 13B", "Meta's 13B parameter open-source language model, known for strong general-purpose performance and efficient fine-tuning capabilities.")
	LLAMA3_8B = ("llama3.1:8b-instruct-q4_K_S", "Llama 3 8B", "The next generation of Llama, with 8 billion parameters and an enhanced 8k-token context window.")
	LLAMA3_2_1B = ("llama3.2:1b-instruct-q4_K_S", "Llama 3.2 1B", "A compact 1B parameter variant in Meta's Llama model series, optimized for efficient deployment while maintaining core language capabilities.")
	LLAMA3_2_3B = ("llama3.2:3b-instruct-q4_K_S", "Llama 3.2 3B", "A 3B parameter model in Meta's Llama series, balancing model size and performance for general language tasks.")
	CODE_LLAMA_7B = ("codellama:7b-instruct-q4_K_S", "CodeLlama 7B", "A 7B parameter variant of Meta's CodeLlama, specifically trained for code generation and understanding across multiple programming languages.")
	CODE_LLAMA_13B = ("codellama:13b-instruct-q4_K_S", "CodeLlama 13B", "The 13B parameter version of CodeLlama, offering enhanced code generation capabilities and deeper programming language understanding compared to the 7B variant.")
	CODE_LLAMA_34B = ("codellama:34b-instruct-q4_K_S", "CodeLlama 34B", "The largest variant of CodeLlama at 34B parameters, providing sophisticated code generation and analysis capabilities across multiple programming languages.")
	GEMMA1_1_2B = ("gemma:2b-instruct-q4_K_S", "Gemma 1.1 2B", "A streamlined LLM with 2 billion parameters and a 4k-token context window, designed for efficient performance.")
	GEMMA1_1_7B = ("gemma:7b-instruct-q4_K_S", "Gemma 1.1 7B", "A larger version of Gemma with 7 billion parameters and a 4k-token context window, offering greater capacity.")
	CODE_GEMMA_1_1_7B = ("codegemma:7b-code-q4_K_S", "Code Gemma 1.1 7B", "A coding-specialized version of Gemma 1.1 with 7 billion parameters and a 4k-token context window.")
	GEMMA2_2B = ("gemma2:2b-instruct-q4_K_S", "Gemma 2 2B", "A compact 2B parameter model from Google's Gemma series, designed for efficient deployment while maintaining strong language understanding capabilities.")
	GEMMA2_9B = ("gemma2:9b-instruct-q4_K_S", "Gemma 2 9B", "The 9B parameter variant of Google's Gemma model, offering enhanced language processing capabilities while remaining relatively efficient to deploy.")
	GEMMA2_27B = ("gemma2:27b-instruct-q4_K_S", "Gemma 2 27B", "The largest model in Google's Gemma series at 27B parameters, designed for high-performance language tasks while maintaining deployment efficiency.")
	GRANITE_3B = ("granite-code:3b-instruct-q4_K_S", "Granite Code 3B", "A versatile model with 3 billion parameters and a 4k-token context window, suitable for lightweight applications.")
	GRANITE_8B = ("granite-code:8b-instruct-q4_K_S", "Granite Code 8B", "A more robust version of Granite, featuring 8 billion parameters and a 4k-token context window for more complex tasks.")
	GRANITE_CODE_3B = ("granite-code:3b-instruct-128k-q4_K_S", "Granite Code 3B 128K", "A 3B parameter code-specialized model from IBM's Granite series, focused on programming language understanding and code generation.")
	GRANITE_CODE_20B = ("granite-code:20b-instruct-q4_K_S", "Granite Code 20B", "A 20B parameter code-focused model from IBM's Granite series, providing advanced code generation and analysis capabilities.")
	GRANITE_CODE_34B = ("granite-code:34b-instruct-q4_K_S", "Granite Code 34B", "The largest code-specialized model in IBM's Granite series at 34B parameters, designed for sophisticated code generation and understanding tasks.")
	GRANITE_3_DENSE_2B = ("granite3-dense:2b-instruct-q4_K_S", "Granite 3 Dense 2B", "A compact 2B parameter dense model from IBM's Granite 3 series, optimized for efficient general-purpose language tasks.")
	GRANITE_3_DENSE_8B = ("granite3-dense:8b-instruct-q4_K_S", "Granite 3 Dense 8B", "An 8B parameter dense model from IBM's Granite 3 series, offering enhanced language capabilities while maintaining efficient computation.")
	GRANITE_3_MOE_1B = ("granite3-moe:1b-instruct-q4_K_S", "Granite 3 MoE 1B", "A 1B parameter mixture-of-experts model from IBM's Granite 3 series, using sparse computation for efficient processing.")
	GRANITE_3_MOE_3B = ("granite3-moe:3b-instruct-q4_K_S", "Granite 3 MoE 3B", "A 3B parameter mixture-of-experts model from IBM's Granite 3 series, combining larger scale with efficient sparse computation.")
	GRANITE_3_1_DENSE_2B = ("granite3.1-dense:2b-instruct-q4_K_S", "Granite 3.1 Dense 2B", "An updated 2B parameter dense model from IBM's Granite 3.1 series, incorporating improvements in general language understanding.")
	GRANITE_3_1_DENSE_8B = ("granite3.1-dense:8b-instruct-q4_K_S", "Granite 3.1 Dense 8B", "An enhanced 8B parameter dense model from IBM's Granite 3.1 series, offering improved language capabilities over the 3.0 version.")
	QWEN_2_5_CODER_0_5B = ("qwen2.5-coder:0.5b-instruct-q4_K_S", "Qwen 2.5 Coder 0.5B", "A highly compact 0.5B parameter code-specialized model from Alibaba's Qwen series, designed for lightweight code generation tasks.")
	QWEN_2_5_CODER_1_5B = ("qwen2.5-coder:1.5b-instruct-q4_K_S", "Qwen 2.5 Coder 1.5B", "A 1.5B parameter code generation model from Qwen, offering enhanced capabilities while maintaining efficient deployment.")
	QWEN_2_5_CODER_3B = ("qwen2.5-coder:3b-instruct-q4_K_S", "Qwen 2.5 Coder 3B", "A 3B parameter code-specialized model from Qwen, providing strong code generation and understanding capabilities.")
	QWEN_2_5_CODER_7B = ("qwen2.5-coder:7b-instruct-q4_K_S", "Qwen 2.5 Coder 7B", "A 7B parameter code generation model from Qwen, offering advanced programming capabilities across multiple languages.")
	QWEN_2_5_CODER_14B = ("qwen2.5-coder:14b-instruct-q4_K_S", "Qwen 2.5 Coder 14B", "A 14B parameter code-focused model from Qwen, providing sophisticated code generation and analysis features.")
	QWEN_2_5_CODER_32B = ("qwen2.5-coder:32b-instruct-q4_K_S", "Qwen 2.5 Coder 32B", "The largest code-specialized model in Qwen's 2.5 series at 32B parameters, designed for complex code generation and understanding tasks.")
	QWEN_QWQ_PREVIEW_32B = ("qwq:32b-preview-q4_K_M", "Qwen QwQ Preview 32B", "A 32B parameter preview model from Qwen's QwQ series, showcasing advanced language understanding and generation capabilities.")
	QWEN_2_5_DEEPSEEK_R1_DISTILL_32B = ("deepseek-r1:32b-qwen-distill-q4_K_M", "DeepSeek 32B", "DeepSeek R1 Distill Qwen 32B is a distilled large language model based on Qwen 2.5 32B, using outputs from DeepSeek R1. It outperforms OpenAI's o1-mini across various benchmarks, achieving new state-of-the-art results for dense models.")
	QWEN_2_5_DEEPSEEK_R1_DISTILL_14B = ("deepseek-r1:14b-qwen-distill-q4_K_M", "DeepSeek 14B", "DeepSeek R1 Distill Qwen 14B is a distilled large language model based on Qwen 2.5 14B, using outputs from DeepSeek R1. It outperforms OpenAI's o1-mini across various benchmarks, achieving new state-of-the-art results for dense models.")
	QWEN_2_5_DEEPSEEK_R1_DISTILL_8B = ("deepseek-r1:8b-llama-distill-q4_K_M", "DeepSeek 8B", "DeepSeek R1 Distill Qwen 8B is a distilled large language model based on Qwen 2.5 8B, using outputs from DeepSeek R1. It outperforms OpenAI's o1-mini across various benchmarks, achieving new state-of-the-art results for dense models.")
	QWEN_2_5_DEEPSEEK_R1_DISTILL_7B = ("deepseek-r1:7b-qwen-distill-q4_K_M", "DeepSeek 7B", "DeepSeek R1 Distill Qwen 7B is a distilled large language model based on Qwen 2.5 7B, using outputs from DeepSeek R1. It outperforms OpenAI's o1-mini across various benchmarks, achieving new state-of-the-art results for dense models.")
	QWEN_2_5_DEEPSEEK_R1_DISTILL_1_5B = ("deepseek-r1:1.5b-qwen-distill-q4_K_M", "DeepSeek 1.5B", "DeepSeek R1 Distill Qwen 1.5B is a distilled large language model based on  Qwen 2.5 Math 1.5B, using outputs from DeepSeek R1. It's a very small and efficient model which outperforms GPT 4o 0513 on Math Benchmarks.")
	STAR_CODER_2_15B = ("starcoder2:15b-instruct-v0.1-q4_K_S", "StarCoder 2 15B", "A 15B parameter code generation model, part of the StarCoder series known for strong performance across multiple programming languages.")

	def __init__(self, unique_id, model_label, model_description):
		self._readable_name = model_label
		self._description = model_description
		self._unique_id = unique_id

	@property
	def readable_name(self):
		return self._readable_name

	@property
	def description(self):
		return self._description

	@property
	def unique_id(self):
		return self._unique_id

	@property
	def model_found(self) -> bool:
		return bool(PiecesSettings._models_map.get(self.unique_id, False))

	@property
	def snapshot(self):
		return PiecesSettings._models_map[self.unique_id]

	@classmethod
	def get(cls, unique_id):
		for model in cls:
			if model.unique_id == unique_id:
				return model
		return None

	@property
	def id(self):
		return self.snapshot.id

	@property
	def model_status(self):
		if self.snapshot.cloud:
			return ModelStatus.cloud
		elif self.snapshot.downloaded:
			return ModelStatus.downloaded
		elif self.snapshot.downloading:
			return ModelStatus.downloading
		else:
			return ModelStatus.download

	@property
	def model_status_readable(self):
		if self.model_status == ModelStatus.cloud:
			return "Cloud"
		elif self.model_status == ModelStatus.downloaded:
			return "On-Device"
		elif self.model_status == ModelStatus.download:
			return "Click to Download"
		else:
			return "Cancel Download"


class PiecesChangeModelCommand(sublime_plugin.ApplicationCommand):
	@check_pieces_os()
	def run(self, unique):
		model = ModelsEnum.get(unique)
		if not model:
			raise ValueError("Invalid model unique id") # That should not happen

		if model.model_status == ModelStatus.download:
			self.download_llm(model)
			return
		elif model.model_status == ModelStatus.downloading:
			self.cancel_download(model)
			return

		settings = PiecesSettings.get_settings()
		settings["model"] = unique
		sublime.save_settings("Pieces.sublime-settings")
		PiecesSettings.on_settings_change()

	def download_llm(self, model):
		if ModelDownloadWS.is_running():
			sublime.message_dialog("Please wait until the current model is downloaded")
			return
		if sublime.ok_cancel_dialog(f"Are you sure you want to download {model.readable_name}?"):
			download_model = PiecesSettings.api_client.model_api.model_specific_model_download(model.id)
			self.model_ws = ModelDownloadWS(PiecesSettings.api_client,download_model.id,self.on_message_callback)
			self.model_ws.start()
			self.progress_bar = ProgressBar(f"Downloading {model.readable_name}",total=100)
			self.progress_bar.start()
			return

	def cancel_download(self,model):
		PiecesSettings.api_client.model_api.model_specific_model_download_cancel(model.id)

	@check_pieces_os(True)
	def input(self,args):
		return ModelsInputHandler()

	def on_message_callback(self, message: ModelDownloadProgress):
		if message.status == ModelDownloadProgressStatusEnum.IN_MINUS_PROGRESS:
			if message.percentage:
				self.progress_bar.update_progress(message.percentage)
		elif message.status == ModelDownloadProgressStatusEnum.CANCELED:
			self.progress_bar.stop("[❌ Canceled]")
		elif message.status == ModelDownloadProgressStatusEnum.COMPLETED:
			self.progress_bar.stop()
		elif message.status == ModelDownloadProgressStatusEnum.FAILED:
			self.progress_bar.stop("[❌ Failed]")
		else:
			self.progress_bar.stop(str(message.status).lower())

		if message.status != ModelDownloadProgressStatusEnum.IN_MINUS_PROGRESS: # clean up
			try:
				self.model_ws.close()
			except:
				self.model_ws.running = False
				if self.model_ws.ws:
					self.model_ws.ws.close()
			delattr(self.model_ws,"instance")
			BaseWebsocket.instances.remove(self.model_ws)


class ModelsInputHandler(sublime_plugin.ListInputHandler):
	def name(self) -> str:
		return "unique"

	def placeholder(self) -> str:
		model = ModelsEnum.get(PiecesSettings.get_settings().get("model"))
		if model:
			return f"Currently using {model.readable_name}"
		return "Select a Model"

	def list_items(self):
		PiecesSettings.update_model_map()
		return [sublime.ListInputItem(
				text=model.readable_name,
				value=model.unique_id,
				details=model.description,
				annotation=model.model_status_readable) for model in ModelsEnum if model.model_found]

