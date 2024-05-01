import urllib.request
import zipfile
import io
import os
import shutil
import sublime
import importlib

__version__ = "0.1"

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
		"version":"1.2.7"
	},
	{
		"dependency":"pydantic",
		"version":"1.10.13"
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
		file_path = os.path.join(project_dir, filename)
		try:
			shutil.move(file_path, path)
		except:
			file_to_remove = os.path.join(path,filename)
			if os.path.isfile(file_to_remove): # Remove a file
				os.remove(file_to_remove)
			else: # Remove the folder
				shutil.rmtree(file_to_remove)
			shutil.move(file_path, path)

	# Remove the temporary directory
	shutil.rmtree(temp_dir)


	reload_dependency()
	print("Successfully downloaded the pieces dependency")



def reload_dependency():
	for dependency in repo_dependencies:
		dependency = dependency["dependency"]
		if dependency.endswith(".py"):
			dependency = dependency[:-3]
		try:
			m = importlib.import_module(dependency)
			importlib.reload(m)
		except:
			pass

def get_dependency_version(dependency):
	if dependency.endswith(".py"):
		dependency = dependency[:-3]
	m = importlib.import_module(dependency)
	
	try:
		return m.__version__
	except:
		if dependency == "aenum":
			return m.version
		else:
			return "unknown"


def download_lib(path):
	dirs = os.listdir(path)
	for dependency_dict in repo_dependencies:
		dependency = dependency_dict["dependency"]
		repo_version = dependency_dict["version"]
		dependency_version = get_dependency_version(dependency)
		
		
		if dependency not in dirs or repo_version != dependency_version:
			return True
	return False



if download_lib(lib_path):
	print("Pieces is downloading some dependencies")
	sublime.set_timeout_async(lambda:download_github_repo('https://github.com/pieces-app/sublime-dependencies', lib_path), 0)







