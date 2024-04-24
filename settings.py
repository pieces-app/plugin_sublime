from typing import Dict,Union
import pieces_os_client as pos_client
import urllib.request
import json
import sublime

from pieces import __version__

def get_models_ids() -> Dict[str, Dict[str, Union[str, int]]]:
    # api_instance = pos_client.ModelsApi(api_client)

    # api_response = api_instance.models_snapshot()
    # models = {model.name: {"uuid":model.id,"word_limit":model.max_tokens.input} for model in api_response.iterable if model.cloud or model.downloading} # getting the models that are available in the cloud or is downloaded
    

    
    # call the api until the sdks updated
    response = urllib.request.urlopen('http://localhost:1000/models').read()
    response = json.loads(response)["iterable"]
    models = {model["name"]:model["id"] for model in response if model["cloud"] or model.get("downloaded",False)}
    return models



class PiecesSettings:
    @classmethod
    def on_settings_change(cls):

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


settings = sublime.load_settings('pieces.sublime-settings')

settings.add_on_change("PIECES_SETTINGS",PiecesSettings.on_settings_change)

