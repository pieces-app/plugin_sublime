![Pieces Sublime Plugin](https://camo.githubusercontent.com/69c990240f877927146712d45be2f690085b9e45b4420736aa373917f8e0b2c8/68747470733a2f2f73746f726167652e676f6f676c65617069732e636f6d2f7069656365735f7374617469635f7265736f75726365732f7066645f77696b692f5049454345535f4d41494e5f4c4f474f5f57494b492e706e67)


##### <p align="center"> [Website](https://pieces.app/) • [Pieces OS Documentation](https://docs.pieces.app/) • [Pieces Sublime github repository](https://github.com/pieces-app/plugin_sublime)
</p>

# Important

Please make sure you have [**Pieces OS**](https://docs.pieces.app/installation-getting-started/what-am-i-installing) installed to run the Pieces CLI tool.


## Getting Started

Welcome to the Pieces Sublime Plugin.
The Pieces Sublime plugin is designed to manage your saved materials in Pieces right from within Sublime, and interact seamlessly with Pieces OS.

To get started, check the settings. If you wish to change the llm model you're using or the host, you can do so in the settings `Preferences > Package Settings > Pieces > Settings`.

### Open Saved Material

To open your saved materials, simply open your command palette and run `Pieces: Open Saved Material`. Then, select the asset you wish to open.

#### Edit Saved Materials

To edit a saved material, you'll need to toggle into editor mode. You can do so by tapping `command/ctrl+e`. From there, you will be able to modify the contents of your material and save the changes using `command/ctrl + s`.

#### Copy Saved Material

If you're viewing a saved material, you can quickly copy the asset content without selecting it using `command/ctrl + c`.

### Right click to add an asset

To save a new snippet in Pieces, select the code you wish to save, right-click to open the context menu, and select `Pieces > Save to Pieces`.

### Copilot Ask

Need the Copilot to comment, fix a bug, or add a doc string? Select some code, right-click to open the context menu, and select Pieces > Ask Copilot.

### Login/Logout

You can log in and out of your Pieces account using the `Pieces: Login` or `Pieces: Logout` command in your command palette. An output panel is available to check your cloud status and login status.

### Connect or Disconnect your Personal Pieces Cloud

You can connect and disconnect from your cloud using `Pieces: Connect Personal Cloud` or `Pieces: Disconnect Personal Cloud` command in your command palette.
Note: In order you use these commands, you must have an account connected to Pieces.

### Find your Saved Materials

You can search a saved material using `Pieces: Search`.

There are three main types of seaching:

- **Fuzzy Search**: Fuzzy Search is a technique used to find matches that are likely to be relevant, even if they are not exact matches. It is particularly useful for handling typos, misspellings, and variations in data.

- **Full Text Search**: Full Text Search is a technique used to search for documents or records that contain the exact sequence of words in the search query. It indexes all the words in a document to enable fast and efficient searching.

- **Neural Code Search**: Neural Code Search is a technique that leverages neural networks and machine learning to improve the search and retrieval of code snippets. It allows you to use natural language to describe what you are looking for, capturing the semantics and context of the code to provide more accurate and relevant results.

### Reload the Plugin

If you're experiencing an issue or something isn't working properly, try reloading the plugin using the command `Pieces: Reload Plugin` in your command palette. Don't forget to make sure Pieces OS is running.

### Get Support or Share Feedback

Experiencing an issue or have feedback for the Pieces team? No worries, we've got you covered. Simply open the command palette and run `Pieces: Get Support`. From here, you will find resources where you can connect with the Pieces team.

## How to install?

### Stable build (Recommended):

- Download the [package control](https://packagecontrol.io/installation)
- Open your command palette. You can use the shortcut key combination `Ctrl+Shift+P` on Windows and `Cmd+Shift+P` on MacOS.
- Search for `Package Control: Install Package`  
- Search for Pieces and select it.
> IMPORTANT: When you first download the package, it will download and install some required dependencies. As a result, you might need to restart Sublime after installing.

### Pre-releases:

You can download and checkout some new beta features before releasing.

- Make sure you have downloaded the [package control](https://packagecontrol.io/installation)
- Download the `Pieces.sublime-package` from [releases](https://github.com/pieces-app/plugin_sublime/releases) on GitHub 
- Add `Pieces.sublime-package` to the Installed Packages directory.
	- **Windows**: %APPDATA%\Sublime Text\Installed Packages
	- **MacOS**: ~/Library/Application Support/Sublime Text 3/Installed Packages
	- **Linux**: ~/.config/sublime-text/Installed Packages
- Open Sublime and enjoy the package


## Connect with the Pieces Community

#### Join our [Discord Community](https://discord.gg/getpieces)

Become a part of our Discord community to stay updated and engage in discussions about our features.

#### Submit a Feature Request or Feedback

Have an idea for a new feature? Feel free to submit your suggestions on our [GitHub page](https://github.com/pieces-app/plugin_sublime/issues).

#### Tech Blogs

Stay connected and up-to-date with our latest [blogs](https://code.pieces.app/blog).

#### Plugins

Explore our collection of awesome Pieces [plugins](https://code.pieces.app/plugins).

#### View Power Tips & Best Practices

Don't forget to check out our YouTube channel for [Power Tips & Best Practices](https://youtube.com/@getpieces)
