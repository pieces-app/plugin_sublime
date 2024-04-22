from typing import Dict,Union
import pieces_os_client as pos_client
import urllib.request
import json
import sublime


def get_models_ids() -> Dict[str, Dict[str, Union[str, int]]]:
    # api_instance = pos_client.ModelsApi(api_client)

    # api_response = api_instance.models_snapshot()
    # models = {model.name: {"uuid":model.id,"word_limit":model.max_tokens.input} for model in api_response.iterable if model.cloud or model.downloading} # getting the models that are available in the cloud or is downloaded
    

    
    # call the api until the sdks updated
    response = urllib.request.urlopen('http://localhost:1000/models').read()
    response = json.loads(response)["iterable"]
    models = {model["name"]:model["id"] for model in response if model["cloud"] or model.get("downloaded",False)}
    return models



models = get_models_ids()

def on_settings_change():
    global host,model_id,api_client,models,WEBSOCKET_URL
    

    # Model
    model_name = settings.get("model")
    default_model_name = "GPT-3.5-turbo Chat Model"

    if model_name:
        model_id = models.get(model_name,None)
        if not model_id:
            print(f"The model that you are using is invaild. Would you please enter a vaild model name \nUsing {default_model_name}")
        else:model_id = models[default_model_name]
    else:model_id = models[default_model_name]
        

    # Host
    host = settings.get('host')
    if not host:
        if 'linux' == sublime.platform():
            host = "http://localhost:5323"
        else:
            host = "http://localhost:1000"

    WEBSOCKET_URL = host.replace('http','ws') + "/qgpt/stream"

    # Defining the host is optional and defaults to http://localhost:1000
    # See configuration.py for a list of all supported configuration parameters.
    configuration = pos_client.Configuration(host=host)


    # Initialize the ApiClient globally
    api_client = pos_client.ApiClient(configuration)




settings = sublime.load_settings('pieces.sublime-settings')

settings.add_on_change("PIECES_SETTINGS",on_settings_change)

on_settings_change()
