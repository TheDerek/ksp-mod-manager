Kerbal Space Program Mod Manager
================================

A desktop mod manager for Kerbal Space Program. Uses kerbalstuff to obtain mods.

![](http://i.imgur.com/90BbiyJ.png)

It SHOULD automaticly detect GameData folders and extract them into the user specified GameData folder. Does not do this with ships and other things though, it just assumes that if a GameData folder is present then other folders such as ships will be in the root directory of the mod archive.

If no GameData folder is present, it simply extracts the entire archive into the given GameData folder.


To Run:
* Install Python 2.7
* Install PyQt
* Git Pull
* Run app.py

Requires:
* PyQt
* Python 2.7

TODO:
* Intergrate download window into main window
* Inform of install succsess/failuire
* Warn of overiding existing installs
* List installed mods, add uninstall/disable option


