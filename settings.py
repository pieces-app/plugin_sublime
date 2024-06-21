from ._pieces_lib import pieces_os_client as pos_client
import sublime
from typing import Dict

from . import __version__



class PiecesSettings:
	# Initialize class variables
	application = None
	models = None
	host = ""
	model_name = ""
	api_client = None
	_is_loaded = False # is the plugin loaded




	@property
	def is_loaded(self):
		sublime.set_timeout_async(self.get_health,0)
		return self._is_loaded



	@is_loaded.setter
	def is_loaded(self,is_loaded):
		self._is_loaded = is_loaded


	@classmethod
	def get_health(cls):
		"""
		Retrieves the health status from the WellKnownApi and returns True if the health is 'ok', otherwise returns False.

		Returns:
		bool: True if the health status is 'ok', False otherwise.
		"""
		try:
			health = pos_client.WellKnownApi(cls.api_client).get_well_known_health()
			health = health == "ok"
			cls._is_loaded = health
			return health
		except:
			return False


	@classmethod
	def host_init(cls,host):
		"""
		Initialize the host URL for the API connection.

		This method sets the host URL based on the configuration settings. If the host URL is not provided in the settings, it defaults to a specific URL based on the platform. 
		It then creates the WebSocket base URL and defines the WebSocket URLs for different API endpoints.
		"""
		cls.host = host
		if not host:
			if 'linux' == sublime.platform():
				cls.host = "http://127.0.0.1:5323"
			else:
				cls.host = "http://127.0.0.1:1000"

		ws_base_url = cls.host.replace('http','ws')

		cls.ASSETS_IDENTIFIERS_WS_URL = ws_base_url + "/assets/stream/identifiers"

		cls.AUTH_WS_URL = ws_base_url + "/user/stream"

		configuration = pos_client.Configuration(host=cls.host)

		cls.api_client = pos_client.ApiClient(configuration)




	@classmethod
	def models_init(cls,model):
		"""
		Initialize the model ID for the class using the specified settings.

		This method retrieves the available models, sets the model ID based on the settings provided,
		and defaults to a specific model ("GPT-3.5-turbo Chat Model") if the specified model is not found.
		"""

		models = cls.get_models_ids()
		cls.model_name = model
		cls.model_id = models.get(str(cls.model_name))

		if not cls.model_id:
			cls.model_id = models["GPT-3.5-turbo Chat Model"]


	@classmethod
	def on_settings_change(cls,all = False):
		"""
			all parameter means to update everything not the changes
		"""
		settings = sublime.load_settings("Pieces.sublime-settings") # Reload the settings
		host = settings.get('host')
		model = settings.get("model")
		if cls.host != host or all:
			cls.host_init(host = host)
			cls.models_init(model = model)

		if cls.model_name != model or all:
			cls.models_init(model = model)
		



	@classmethod
	def get_application(cls)-> pos_client.Application:
		if cls.application:
			return cls.application

		# Decide if it's Windows, Mac, Linux or Web
		api_instance = pos_client.ConnectorApi(cls.api_client)
		seeded_connector_connection = pos_client.SeededConnectorConnection(
			application=pos_client.SeededTrackedApplication(
				name = "SUBLIME",
				platform = sublime.platform().upper() if sublime.platform() != 'osx' else "MACOS",
				version = __version__))
		api_response = api_instance.connect(seeded_connector_connection=seeded_connector_connection)
		cls.application = api_response.application
		return cls.application

	@classmethod
	def get_models_ids(cls) -> Dict[str, str]:
		if cls.models:
			return cls.models

		api_instance = pos_client.ModelsApi(cls.api_client)

		api_response = api_instance.models_snapshot()
		cls.models = {model.name: model.id for model in api_response.iterable if model.cloud or model.downloaded} # getting the models that are available in the cloud or is downloaded


		return cls.models


	@classmethod
	def create_auth_output_panel(cls):
		window = sublime.active_window()
		cls.output_panel = window.create_output_panel("Pieces Auth")
		cls.output_panel.settings().set("line_numbers", False)  # Disable line numbers
		cls.output_panel.settings().set("gutter", False)
		cls.output_panel.set_read_only(True)

