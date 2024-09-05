from ._pieces_lib.pieces_os_client import SeededConnectorConnection,SeededTrackedApplication
from ._pieces_lib.pieces_os_client.wrapper.websockets.base_websocket import BaseWebsocket
from ._pieces_lib.pieces_os_client.wrapper import PiecesClient
from multiprocessing.pool import ThreadPool
import sublime
import os

from . import __version__



class PiecesSettings:
	# Initialize class variables
	api_client = PiecesClient(seeded_connector= SeededConnectorConnection(
			application=SeededTrackedApplication(
				name = "SUBLIME",
				platform = sublime.platform().upper() if sublime.platform() != 'osx' else "MACOS",
				version = __version__)))
	_pool = None
	is_loaded = False # is the plugin loaded
	health = "failed"
	ONBOARDING_SYNTAX = "Packages/Pieces/syntax/Onboarding.sublime-syntax"
	on_model_change_callbacks = [] # If the model change a function should be runned

	PIECES_USER_DIRECTORY = os.path.join(sublime.packages_path(),"User","Pieces")

	autocomplete_snippet:bool = True 
	# Create the pieces directory to store the data if it does not exists
	if not os.path.exists(PIECES_USER_DIRECTORY):
		os.makedirs(PIECES_USER_DIRECTORY)


	@classmethod
	def host_init(cls,host):
		"""
		Initialize the host URL for the API connection.

		This method sets the host URL based on the configuration settings. If the host URL is not provided in the settings, it defaults to a specific URL based on the platform. 
		It then creates the WebSocket base URL and defines the WebSocket URLs for different API endpoints.
		"""
		if host != cls.api_client.host:
			cls.api_client.init_host(host)
			BaseWebsocket.reconnect_all()


	@classmethod
	def models_init(cls,model):
		"""
		Initialize the model ID for the class using the specified settings.

		This method retrieves the available models, sets the model ID based on the settings provided,
		and defaults to a specific model ("GPT-3.5-turbo Chat Model") if the specified model is not found.
		"""

		models = cls.api_client.get_models()
		cls.model_name = model
		cls.model_id = models.get(str(cls.model_name))

		if not cls.model_id:
			cls.model_id = models["GPT-3.5-turbo Chat Model"]
		for func in cls.on_model_change_callbacks:
			func()

	@classmethod
	def on_settings_change(cls,all = False):
		"""
			all parameter means to update everything not the changes
		"""
		settings = cls.get_settings()
		cls.autocomplete_snippet = bool(settings.get("snippet.autocomplete",True))
		host = settings.get('host')
		model = settings.get("model")
		if cls.api_client.host != host or all:
			cls.host_init(host = host)
			cls.models_init(model = model)

		if cls.model_name != model or all:
			cls.models_init(model = model)

	@staticmethod
	def get_settings():
		return sublime.load_settings("Pieces.sublime-settings") # Reload the settings

	@classmethod
	def create_auth_output_panel(cls):
		window = sublime.active_window()
		cls.output_panel = window.create_output_panel("Pieces Auth")
		cls.output_panel.settings().set("line_numbers", False)  # Disable line numbers
		cls.output_panel.settings().set("gutter", False)
		cls.output_panel.set_read_only(True)

	@classmethod
	def pool(cls):
		"""Create thread pool on first request
		 avoids instantiating unused threadpool for blocking clients.
		"""
		if cls._pool is None:
			cls._pool = ThreadPool(1)
		return cls._pool

	# Load the settings from 'Pieces.sublime-settings' file using Sublime Text API
	pieces_settings = sublime.load_settings('Pieces.sublime-settings')
	pieces_settings.add_on_change("PIECES_SETTINGS",on_settings_change)

