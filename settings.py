import pieces_os_client as pos_client
import sublime

from pieces import __version__



class PiecesSettings:
    @classmethod
    def on_settings_change(cls):
        settings = sublime.load_settings('pieces.sublime-settings')
        
        # Host
        cls.host = settings.get('host')
        if not cls.host:
            if 'linux' == sublime.platform():
                cls.host = "http://localhost:5323"
            else:
                cls.host = "http://localhost:1000"


        ws_base_url = cls.host.replace('http','ws')

        # WEBSOCKET_URL = ws_base_url + "/qgpt/stream"

        cls.ASSETS_IDENTIFIERS_WS_URL = ws_base_url + "/assets/stream/identifiers"

        # Defining the host is optional and defaults to http://localhost:1000
        # See configuration.py for a list of all supported configuration parameters.
        configuration = pos_client.Configuration(host=cls.host)


        # Initialize the ApiClient globally
        cls.api_client = pos_client.ApiClient(configuration)

    @classmethod
    def get_application(cls)-> pos_client.Application:
        if cls.application:
            return application

        # Decide if it's Windows, Mac, Linux or Web
        api_instance = pos_client.ConnectorApi(cls.api_client)
        seeded_connector_connection = pos_client.SeededConnectorConnection(
            application=pos_client.SeededTrackedApplication(
                name = "SUBLIME",
                platform = sublime.platform().upper() if sublime.platform() != 'osx' else "MACOS",
                version = __version__))
        api_response = api_instance.connect(seeded_connector_connection=seeded_connector_connection)
        return api_response.application

