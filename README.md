# [Pieces for Developers](https://pieces.app/plugins/sublime) | Sublime Plugin

![Pieces Sublime Plugin](icons/hero-image.png)

##### <p align="center"> [Website](https://pieces.app/) • [PiecesOS Documentation](https://docs.pieces.app/) • [Pieces for Sublime Docs](https://docs.pieces.app/extensions-plugins/sublime)
</p>

# Important

Please make sure you have [**PiecesOS**](https://docs.pieces.app/installation-getting-started/what-am-i-installing) installed to run [**the Package.**](https://packagecontrol.io/packages/Pieces) 

## Getting Started with the Pieces Sublime Plugin

Welcome to the **Pieces Sublime Plugin**!

The Pieces Sublime plugin is your gateway to managing your saved code snippets in Pieces directly inside Sublime Text. Seamlessly interact with PiecesOS and enhance your productivity with code snippet management, in-window generative AI conversations, intelligent snippet searching, and AI debugging and code commenting.

## Configuration

Before diving in, let's ensure everything is set up to your liking. You can customize the LLM model or some other settings by navigating to:
`Preferences > Package Settings > Pieces > Settings`.

You can also open the settings from the command palette `Pieces: Open Settings`.

![Pieces Open Settings](icons/pieces%20open%20settings.png)

#### LLMs Supported by the Pieces for Sublime Plugin 

Currently, the Pieces for Sublime Plugin supports 20+ AI models, so you can choose the one that best fits your needs.

![Pieces Change LLM](icons/pieces%20change%20llm.png)

- GPT-4o Mini
- GPT-4o
- GPT-4 Turbo
- GPT-4
- GPT-3.5 Turbo
- PaLM 2 Code Chat Bison
- Gemini Pro Chat
- PaLM 2 Chat Bison
- Gemini 1.5 Pro
- Gemini 1.5 Flash
- Claude 3.5 Sonnet
- Claude 3 Sonnet
- Claude 3 Opus
- Claude 3 Haiku
- Mistral 7B
- Phi-3 Mini 4K
- Phi-3 Mini 128K
- Phi-2
- LLaMA 3 8B
- LLaMA 2 7B
- Gemma 1.1 7B
- Gemma 1.1 2B
- Code Gemma 1.1 7B
- Granite 8B
- Granite 3B

## Features
### Logging Into or Out Of Pieces Account

Using the command `Pieces: Connect Personal Cloud` or `Pieces: Disconnect Personal Cloud` from your command palette logs you in and out of your Pieces account. An output panel is available to check your cloud status and login status.

Logging into your Pieces account lets you sync your snippets and settings between PiecesOS and other Pieces plugins. 

### Right Click to Save to Pieces

Saving a new snippet in Pieces is a breeze! Just select the code you want to save, right-click to open the context menu, and choose `Pieces > Save to Pieces`. Your code is now safely stored!

![save to pieces](icons/pieces%20save%20to%20pieces.png)

### Engage with the Pieces Copilot

You can ask the Pieces Copilot questions about your code, view your conversations list, or start a new conversation by opening the command palette and entering `Pieces: Copilot`. Your selected LLM will then output an answer as a generation on the right side of your screen, right in your Sublime Text editor window.

![pieces copilot](icons/pieces%20pieces%20copilot.png)

### Copilot Ask

Need some help from the Pieces Copilot? Just select the code and right-click to open the context menu and choose `Pieces > Ask Copilot`. 

![copilot ask](icons/pieces%20ask%20copilot.png)

#### AI Debugging

You can utilize the LLM capabilities of Pieces Copilot with an intelligent debugging feature, helping you identify errors in your code and preview potential solutions before applying changes.

![debugging](icons/pieces%20debugging%20tool.png)

#### Code Comments

The mark of well-written, high-quality code (aside from functionality!) is code comments. This can get tedious, though, so the Pieces for Sublime Plugin comes with a built-in intelligent commenting feature. Selecting the `Add code comments` option from the context menu will add comments to your selected portion of code. 

Let Copilot do the heavy lifting for you!

![code comments](icons/pieces%20add%20code%20comments.png)

### Ask about the current Project or File

The Pieces for Sublime Plugin lets you ask context-focused questions based on the file you're working in, or the entire project itself. This is an extremely useful feature for new developers getting to know an unfamiliar codebase just as well as experienced developers looking to cut down on production time.

- **Ask About the Current Project**: Use the command `Pieces: Ask about the current project` to ask the Pieces Copilot a question about your entire project. 
- **Ask About the Current File**: Use the command `Pieces: Ask about the current file` to get assistance with the current opened file.

![ask about current file and project](icons/pieces%20ask%20about%20current%20file.png)

### Sublime Snippet Management

You can import and export code snippets you've saved using other Pieces software for use in or from Sublime. 

- **Import Sublime Snippet**: Use the command `Pieces: Import Sublime Snippet` to import a Sublime snippet into Pieces.
- **Export Pieces Material**: Use the command `Pieces: Export Pieces Material` to export a Pieces snippet back to Sublime.

### Open Saved Materials

Ready to access your saved materials? It's super easy! Just follow these steps:

1. Open your command palette (`Ctrl+Shift+P` or `Cmd+Shift+P`).
2. Run the command: `Pieces: Open Saved Material`.
3. Select the asset you wish to open from the list.

![open saved materials](icons/pieces%20open%20saved%20material.png)

Your material is now open and ready for you to use. 

### Find your Saved Code Snippets

You can search for saved snippets using `Pieces: Search`.

There are [three types of searching:](https://docs.pieces.app/features/search-modes)

- **Fuzzy Search**: Fuzzy Search finds snippets that are likely to be relevant, even if they are not exact matches. It is particularly useful for handling typos, misspellings, and variations in data.

- **Full-Text Search**: Full-Text Search is a technique used to search for documents or records that contain the exact sequence of words in the search query. It indexes all the words in a document to enable fast and efficient searching.

- **Neural Code Search**: Neural Code Search leverages neural networks and machine learning to improve the search and retrieval of code snippets. It allows you to use natural language to describe what you are looking for, capturing the semantics and context of the code to provide more accurate and relevant results.

### Edit Saved Materials

Want to make [changes to your saved materials?](https://docs.pieces.app/features/managing-saved-materials) 

Switch to editor mode by clicking the **Edit** button on your saved snippet. Modify the content as needed and save your changes with a simple `command/ctrl + s`. 

### Shareable Link

If you want to [share a saved snippet](https://docs.pieces.app/features/one-click-snippet-sharing) with another developer (even if they don't have a Pieces account), you can. 

Just select the code, right-click to open the context menu, and choose `Pieces > Generate shareable link`. 

You can also share a saved snippet by opening it with `Pieces: Open saved Material` and clicking the **Share** button. 

### [Auto Complete](https://docs.pieces.app/features/code-completion)

Enhance your coding speed with auto-completion using saved Pieces Snippets. When you have Pieces Snippets saved, you will receive automatic code completions tailored to specific programming languages.

You can enable or disable this feature in your settings by entering `Pieces: Open Pieces Settings` in your command palette. Then, overwrite the `snippet.autocomplete` object to `false` to turn the auto-completion feature off.

### Reload the Plugin

If you're experiencing an issue or something isn't working properly, try reloading the plugin using the command `Pieces: Reload Plugin` in your command palette. 

Don't forget to make sure PiecesOS is running.

### Get Support or Share Feedback

Experiencing an issue or have feedback for the Pieces team? 

No worries, we've got you covered. 

Simply open the command palette and run `Pieces: Get Support`. From here, you will find resources where you can connect with the Pieces team.

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

### Privacy and Data Collection

We take your privacy seriously. We are committed to ensuring that your data remains private and secure. To that end, we want to make it clear that:

**We do not collect any client-side telemetry.**

[Read more about data collection and privacy](https://docs.pieces.app/product-highlights-and-benefits/privacy-security-data)
