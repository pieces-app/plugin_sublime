# This is the development readme for Sublime Plugin

### Installing a staging build

In order to install a staging build:

1. Download the Staging build "Pieces.sublime-package" from "https://github.com/pieces-app/plugin_sublime/releases"
2. Place it in the installed package directory 
  - **Windows**: `%APPDATA%\Sublime Text\Installed Packages`
  - **MacOS**: `~/Library/Application Support/Sublime Text 3/Installed Packages`
  - **Linux**: `~/.config/sublime-text/Installed Packages`

### Outlines the development set up and general practices

### Setup:

1. Open your terminal and change directory (`cd`) to 
  - **Windows**: `%APPDATA%\Sublime Text\Packages`
  - **MacOS**: `~/Library/Application Support/Sublime Text 3/Packages`
  - **Linux**: `~/.config/sublime-text/Packages`
2. run `git clone https://github.com/pieces-app/plugin_sublime.git`
3. happy coding :)

### Dependency management

You can manage dependencies two ways:

- Add the dependency in the `dependencies.json` if it **exists** (here)[https://github.com/packagecontrol/channel/blob/main/repository.json]
- Follow the steps (here)[https://github.com/pieces-app/plugin_sublime_dependencies?tab=readme-ov-file]

### Trigger a Release

- OPTIONAL: Create a message for the users (release notes) in the `messages/<new version>`
  and then configure it in the `messages.json` file
- Update the `_version.py` with the appropriate version 
- `git tag <new version> main`
- `git push origin tag <new version>`

