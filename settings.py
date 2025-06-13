import webbrowser

from ._pieces_lib.pieces_os_client.models.application_name_enum import ApplicationNameEnum
from ._pieces_lib.pieces_os_client import SeededConnectorConnection,SeededTrackedApplication, ApplicationsApi
from ._pieces_lib.pieces_os_client.wrapper.websockets.base_websocket import BaseWebsocket
from ._pieces_lib.pieces_os_client.wrapper import PiecesClient
from ._pieces_lib.pieces_os_client.wrapper.version_compatibility import VersionCheckResult
from multiprocessing.pool import ThreadPool
import sublime
import os
from .assets.ext_map import file_map

from ._version import __version__
from enum import Enum
import webbrowser
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

try:
	from . import _debug
	debug = True
	print("RUNNING DEBUG MODE")
except:
	debug = False

class CopilotMode(Enum):
	IDE = "IDE"
	BROWSER = "BROWSER"

	@staticmethod
	def parse(string: str):
		if string.upper() == "IDE":
			return CopilotMode.IDE
		elif string.upper() == "BROWSER":
			return CopilotMode.BROWSER
		else:
			sublime.error_message("Invalid settings for Copilot it should be IDE or BROWSER")
			return CopilotMode.IDE



class PiecesSettings:
	# Initialize class variables
	api_client = PiecesClient(seeded_connector= SeededConnectorConnection(
			application=SeededTrackedApplication(
				name = "SUBLIME",
				platform = sublime.platform().upper() if sublime.platform() != 'osx' else "MACOS",
				version = __version__)),
	connect_websockets = False,
	reconnect_on_host_change = False)
	_pool = None
	_os_id = None
	debug=debug
	copilot_mode: CopilotMode = CopilotMode.IDE
	ONBOARDING_SYNTAX = "Packages/Pieces/syntax/Onboarding.sublime-syntax"
	on_model_change_callbacks = [] # If the model change a function should be runned

	PIECES_USER_DIRECTORY = os.path.join(sublime.packages_path(),"User","Pieces")

	autocomplete_snippet:bool = True 
	# Create the pieces directory to store the data if it does not exists
	if not os.path.exists(PIECES_USER_DIRECTORY):
		os.makedirs(PIECES_USER_DIRECTORY)

	_update_dict = {}
	_models_map = {}

	@classmethod
	def update_model_map(cls):
		cls._models_map = {model.unique : model for model in PiecesSettings.api_client.models_api.models_snapshot().iterable if model.unique}


	@classmethod
	def models_init(cls,model):
		"""
		Initialize the model ID for the class using the specified settings.

		This method retrieves the available models, sets the model ID based on the settings provided,
		and defaults to a specific model ("GPT 4o") if the specified model is not found.
		"""
		if not cls._models_map:
			cls._models_map = {model.unique : model for model in PiecesSettings.api_client.models_object if model.unique}
		model_id = cls._models_map.get(model)
		if not model_id:
			cls._models_map["gpt-4o"]
		cls.api_client.model_id = model_id.id
		for func in cls.on_model_change_callbacks:
			func()
	@classmethod
	def on_settings_change(cls):
		"""
			all parameter means to update everything not the changes
		"""
		settings = cls.get_settings()
		cls.copilot_mode = CopilotMode.parse(settings.get("copilot"))
		cls.autocomplete_snippet = bool(settings.get("snippet.autocomplete",False))
		model = settings.get("model")

		if cls.api_client.model_name != model:
			cls.models_init(model = model)

		syntax = settings.get("syntax")

		if cls._update_dict != syntax:
			file_map.update(syntax) # Update the file map
			cls._update_dict = syntax


	@staticmethod
	def get_settings():
		return sublime.load_settings("Pieces.sublime-settings") # Reload the settings
	
	@staticmethod
	def output_panel():
		window = sublime.active_window()
		output_panel = window.find_output_panel("Pieces Auth")
		if not output_panel:
			output_panel = window.create_output_panel("Pieces Auth")
			output_panel.settings().set("line_numbers", False)  # Disable line numbers
			output_panel.settings().set("gutter", False)
			output_panel.set_read_only(True)
		return output_panel

	@classmethod
	def pool(cls):
		"""Create thread pool on first request
		 avoids instantiating unused threadpool for blocking clients.
		"""
		if cls._pool is None:
			cls._pool = ThreadPool(1)
		return cls._pool

	@classmethod
	def get_os_id(cls):
		if cls._os_id:
			return cls._os_id
		if not hasattr(cls.api_client, "applications_api"):
			setattr(cls.api_client, "applications_api",
					ApplicationsApi(cls.api_client.api_client))
		for app in cls.api_client.applications_api.applications_snapshot().iterable:
			if app.name == ApplicationNameEnum.OS_SERVER:
				cls._os_id = app.id
				return app.id

	@classmethod
	def open_website(cls, url:str):
		webbrowser.open(cls.add_params(url))

	@classmethod
	def add_params(cls, url:str):
		from .auth.auth_user import AuthUser
		if (not cls.api_client.is_pos_stream_running) or ("pieces.app" not in url):
			return url
		para = {}
		if AuthUser.user_profile:
			para["user"] = AuthUser.user_profile.id
		_id = cls.get_os_id()
		if _id:
			para["os"] = _id

		url_parts = list(urlparse(url))
		query = dict(parse_qsl(url_parts[4]))
		query.update(para)

		url_parts[4] = urlencode(query)
		new_url = urlunparse(url_parts)
		return new_url