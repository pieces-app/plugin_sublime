from ._pieces_lib.pieces_os_client import SeededConnectorConnection,SeededTrackedApplication
from ._pieces_lib.pieces_os_client.wrapper.websockets.base_websocket import BaseWebsocket
from ._pieces_lib.pieces_os_client.wrapper import PiecesClient
from ._pieces_lib.pieces_os_client.wrapper.version_compatibility import VersionCheckResult
from ._pieces_lib import notify as notification
from multiprocessing.pool import ThreadPool
import sublime
import os
from .assets.ext_map import file_map

from . import __version__


try:
	from . import _debug
	debug = True
	print("RUNNING DEBUG MODE")
except:
	debug = False


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
	debug=debug
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


	@staticmethod
	def notify(title,message,level="info"):
		try:
			if level == "error":
				notification.error(title, message, False)
			elif level == "warning":
				notification.warning(title, message, False)
			else:
				notification.info(title, message, False)
			notification.destroy()
		except:
			pass

	if api_client.local_os == "MACOS":
		os_icon = "pieces_server.icns"
	elif api_client.local_os ==  "WINDOWS":
		os_icon = "pieces_server.ico"
	else:
		os_icon = "pieces_server.png"

	package_path = os.path.join(sublime.packages_path(),"Pieces") if debug else os.path.join(sublime.installed_packages_path(),"Pieces.sublime-package")
	path = os.path.join(package_path,"icons", os_icon) if os_icon else None
	os_icon = path
	notification.setup_notifications("Pieces for Sublime Text",os_icon,sender=None)

	# Load the settings from 'Pieces.sublime-settings' file using Sublime Text API
	pieces_settings = sublime.load_settings('Pieces.sublime-settings')
	pieces_settings.add_on_change("PIECES_SETTINGS",on_settings_change)

