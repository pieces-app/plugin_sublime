import urllib.request
import zipfile
import io
import os
import shutil
import sublime

lib_path = os.path.join(os.path.dirname(sublime.packages_path()),"Lib","python38")

dependencies = ["aenum","dateutil","pieces_os_client","pydantic","urllib3","websockets","six.py","typing_extensions.py"]

def download_github_repo(url, path):
    if not url.endswith('/'):
        url += '/'

    url += 'archive/master.zip'

    response = urllib.request.urlopen(url)
    z = zipfile.ZipFile(io.BytesIO(response.read()))

    # Create a temporary directory to extract files to
    temp_dir = os.path.join(path,"TEMP_PIECES")
    z.extractall(temp_dir)

    # Get the name of the directory that was created in the zip
    project_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])

    # Move the files from the project directory to the desired path
    for filename in os.listdir(project_dir):
        try:
            shutil.move(os.path.join(project_dir, filename), path)
        except:
            pass

    # Remove the temporary directory
    shutil.rmtree(temp_dir)

def download_lib(path):
    dirs = os.listdir(path)
    for dependency in dependencies:
        if dependency not in dirs:
            return True
    return False



if download_lib(lib_path):
    print("Pieces is downloading some dependencies")
    sublime.set_timeout_async(lambda:download_github_repo('https://github.com/pieces-app/sublime-dependencies', lib_path), 0)


__version__ = "0.1"

