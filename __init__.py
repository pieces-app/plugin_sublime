import urllib.request
import zipfile
import io
import os
import shutil
import sublime
import importlib
import sublime_plugin
import sys

__version__ = "0.1"

class PiecesDependencies:
	downloading = True
	pieces_plugins = ["pieces.api","pieces.base_websocket","pieces.event_listener",
					"pieces.settings","pieces.main"]
	repo_dependencies = [
		{
			"dependency":"aenum",
			"version":(3,1,15)
		},
		{
			"dependency":"dateutil",
			"version":"2.9.0.post0"
		},
		{
			"dependency":"pieces_os_client",
			"version":"2.2.0"
		},
		{
			"dependency":"pydantic",
			"version":"1.10.15"
		},
		{
			"dependency":"urllib3",
			"version":"2.2.1"
		},
		{
			"dependency":"websockets",
			"version":"12.0"
		},
		{
			"dependency":"six.py",
			"version":"1.16.0"
		},
		{
			"dependency":"typing_extensions.py",
			"version":"unknown"
		}] # Need to be changed each release


	lib_path = os.path.join(os.path.dirname(sublime.packages_path()),"Lib","python38")


	@classmethod
	def download_github_repo(cls,url, version, path):
		if not url.endswith('/'):
			url += '/'

		url += f'releases/download/{version}/dependencies.zip'

		response = urllib.request.urlopen(url)
		z = zipfile.ZipFile(io.BytesIO(response.read()))

		# Create a temporary directory to extract files to
		temp_dir = os.path.join(path, "TEMP_PIECES")
		z.extractall(temp_dir)


		# Move the files from the project directory to the desired path
		for filename in os.listdir(temp_dir):
			file_path = os.path.join(temp_dir, filename)
			try:
				shutil.move(file_path, path)
			except:
				file_to_remove = os.path.join(path, filename)
				if os.path.isfile(file_to_remove):  # Remove a file
					os.remove(file_to_remove)
				else:  # Remove the folder
					shutil.rmtree(file_to_remove)
				shutil.move(file_path, path)

		# Remove the temporary directory
		shutil.rmtree(temp_dir)

		print("Successfully downloaded the pieces dependency")

		cls.reload_dependency() # Reload everything!
		cls.downloading = False

	@classmethod
	def reload_dependency(cls):
		for dependency in cls.repo_dependencies:
			dependency = dependency["dependency"]
			if dependency.endswith(".py"):
				dependency = dependency[:-3]
			try:
				m = importlib.import_module(dependency)
				importlib.reload(m)
			except:
				pass
		
		for plugin in cls.pieces_plugins:
			sublime_plugin.reload_plugin(plugin)
		print("It is recommended to reload sublime since there are some dependencies downloaded")

	@staticmethod
	def get_dependency_version(dependency):
		if dependency.endswith(".py"):
			dependency = dependency[:-3]
		m = importlib.import_module(dependency)
		
		try:
			return m.__version__
		except:
			try:
				return m.version
			except:
				return "unknown"

	@classmethod
	def download_lib(cls):
		dirs = os.listdir(cls.lib_path)
		for dependency_dict in cls.repo_dependencies:
			dependency = dependency_dict["dependency"]
			repo_version = dependency_dict["version"]
			if dependency not in dirs: # Dependency is not found
				return True
			try:
				dependency_version = cls.get_dependency_version(dependency)
			except:
				return True
			
			if repo_version != dependency_version:
				return True
		return False

	@classmethod
	def handle_exception(cls,exc_type, exc_value, exc_traceback):
		# You could also log to a file or display a message to the user
		if exc_type == ModuleNotFoundError and cls.downloading: # override the module not found error until the dependencies are downloaded
			pass
		else:
			# Re-raise the exception to maintain default behavior
			sys.__excepthook__(exc_type, exc_value, exc_traceback)
	
	@classmethod
	def unload_pieces_plugins(cls):
		for plugin in cls.pieces_plugins:
			sublime_plugin.unload_plugin(plugin)

if PiecesDependencies.download_lib():
	# Install the exception handler
	sys.excepthook = PiecesDependencies.handle_exception
	check = True
else: 
	check = False
	PiecesDependencies.downloading = False	


def plugin_loaded(): # Call the download github on the plugin load to avoid duplicated calls
	if check:
		PiecesDependencies.unload_pieces_plugins() # Unload all the plugins
		print("Pieces is downloading some dependencies")
		sublime.set_timeout_async(lambda:PiecesDependencies.download_github_repo('https://github.com/pieces-app/sublime-dependencies', "1.0.3" ,PiecesDependencies.lib_path), 0)
		
