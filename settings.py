from ._pieces_lib.pieces_os_client import SeededConnectorConnection,SeededTrackedApplication
from ._pieces_lib.pieces_os_client.wrapper.websockets.base_websocket import BaseWebsocket
from ._pieces_lib.pieces_os_client.wrapper import PiecesClient
from ._pieces_lib.pieces_os_client.wrapper.version_compatibility import VersionCheckResult
from ._pieces_lib import notify as notification
from multiprocessing.pool import ThreadPool
import sublime
import os

from . import __version__


try:
	from . import _debug
	debug = True
	print("RUNNING DEBUG MODE")
except:
	debug = False


class PiecesSettings:
	# Initialize class variables
	compatiablity_result = VersionCheckResult(True,None) # is it compatiable with the current PiecesOS version?
	api_client = PiecesClient(seeded_connector= SeededConnectorConnection(
			application=SeededTrackedApplication(
				name = "SUBLIME",
				platform = sublime.platform().upper() if sublime.platform() != 'osx' else "MACOS",
				version = __version__)),
	connect_wesockets=False)
	_pool = None
	debug=debug
	is_loaded = False # is the plugin loaded
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
		if host != cls.api_client.host and host:
			cls.api_client.host = host

		if BaseWebsocket.instances:
			BaseWebsocket.reconnect_all()


	@classmethod
	def models_init(cls,model):
		"""
		Initialize the model ID for the class using the specified settings.

		This method retrieves the available models, sets the model ID based on the settings provided,
		and defaults to a specific model ("GPT-3.5-turbo Chat Model") if the specified model is not found.
		"""
		try:
			cls.api_client.model_name = model
		except ValueError:
			sublime.error_message(f"Invalid model\n Choose one from {' ,'.join(cls.api_client.available_models_names)}")
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

		elif cls.api_client.model_name != model:
			cls.models_init(model = model)

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

	# Load the settings from 'Pieces.sublime-settings' file using Sublime Text API
	pieces_settings = sublime.load_settings('Pieces.sublime-settings')
	pieces_settings.add_on_change("PIECES_SETTINGS",on_settings_change)

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

