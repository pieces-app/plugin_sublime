print("This script copyright nathan@pieces.app")

import sys
import os
import re
import zipfile
import compileall
from fnmatch import fnmatch

n = str(sys.argv[1])
print(n)

# The Package Name
package_name = "Pieces"

# Stores Pieces.sublime-package in dir higher
package_destination = "../"

# None ~ Uses Default Settings
profile=None

# Referencing entire repo (where script lives)
package_dir = "."

# Extension
package_filename = package_name + '.sublime-package'

# Where the compiled package will live
package_path = os.path.join(package_destination, package_filename)

if os.path.exists(package_path):
    os.remove(package_path)

# Real Important Zip compression logic
package_file = zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED)

# This must be done exactly like this
# Refer to https://github.com/wbond/package_control/blob/cfaaeb57612023e3679ecb7f8cd7ceac9f57990d/package_control/package_manager.py#L886
# (Hopefully the above file still exists)
compileall.compile_dir(package_dir, quiet=True, legacy=True, optimize=2)

#Keeping these blank, can probs remove but will have to spend time figureing out if it will break code below
dirs_to_ignore = []
files_to_ignore = []
files_to_include = []

slash = '\\' if os.name == 'nt' else '/'
trailing_package_dir = package_dir + slash if package_dir[-1] != slash else package_dir
package_dir_regex = re.compile('^' + re.escape(trailing_package_dir))
for root, dirs, files in os.walk(package_dir):
    # add "dir" to "paths" list if "dir" is not in "dirs_to_ignore"
    dirs[:] = [x for x in dirs if x not in dirs_to_ignore]
    paths = dirs
    paths.extend(files)
    for path in paths:
        full_path = os.path.join(root, path)
        relative_path = re.sub(package_dir_regex, '', full_path)

        ignore_matches = [fnmatch(relative_path, p) for p in files_to_ignore]

        include_matches = [fnmatch(relative_path, p) for p in files_to_include]

        # This is probably done when Package Control rips settings from sublime.py (which references sublime_api.py which is closed sources)
        if ".pyc" in relative_path:
            continue

        # Don't include this script in the package
        if "package.py" in relative_path:
            continue

        #Probably Does what is mentioned above
        if any(ignore_matches) and not any(include_matches):
            continue

        # Ditto
        if os.path.isdir(full_path):
            continue

        # Yee'ol write
        package_file.write(full_path, relative_path)

# We done here
package_file.close()
